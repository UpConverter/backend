import hashlib
import json

import pyvisa
from pyvisa.errors import VisaIOError

from src.attempt.constants import MAIN_CAL
from src.config import settings
from src.connection.models import Connections
from src.visa.exceptions import (
    CalModelSmdvaError,
    ConnectedToSAError,
    ConnectError,
    InvalidConncetionError,
    InvalidDeviceModelError,
    InvalidDeviceNameError,
    InvalidDeviceStateError,
    InvalidSerialNumberError,
    ManySADevicesError,
    SANotExistError,
    VisaError,
)

PORT_MAPPING = {
    "COM1": settings.COM1,
    "COM2": settings.COM2,
    "COM3": settings.COM3,
    "COM4": settings.COM4,
}


class DeviceManager:
    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.device = None
        self.port = None
        self.speed = None
        self.token = None
        self.cals = []
        self.upconv = []

    def __generate_token(self, port, speed, cals, upconv):
        # Создание словаря с данными
        data = {
            "port": port,
            "speed": speed,
            "cals": cals,
            "upconv": upconv,
        }
        # Преобразование словаря в JSON
        json_data = json.dumps(data, sort_keys=True)

        # Генерация хэш-суммы токена
        token = hashlib.md5(json_data.encode()).hexdigest()

        return token

    def __to_dict(self, devices: Connections):
        result = {}
        index = 1

        for device in devices:
            device_dict = {
                "index": index,
                "device_id": device.device_id,
                "model_name": device.model_name,
                "state_name": device.state_name,
                "additional_state_name": device.additional_state_name,
                "serial_number": device.serial_number,
                "connected_to_device": device.connected_to_device,
                "connected_to_device_model_name": device.connected_to_device_model_name,
                "connected_to_device_channel": device.connected_to_device_channel,
            }
            result[device.device] = device_dict
            index += 1

        return result

    def __parse_response(self, res: str):
        return res.split(" ")[0]

    def __connect(self, port, speed) -> bool:
        if self.device is not None and self.port == port and self.speed == speed:
            return True

        try:
            # Если подключен с другими параметрами, то надо переподключить
            if self.device is not None:
                if settings.ENVIRONMENT.is_debug:
                    print(
                        "\033[93mИзменились параметры подключения. Переподключим устройство",
                        self.device,
                        "\033[0m",
                    )
                self.device.close()
                self.device = None

            self.port = port
            self.speed = speed
            self.device = self.rm.open_resource(PORT_MAPPING.get(port))
            self.device.baud_rate = speed
            return True

        except VisaIOError:
            raise VisaError()

        except Exception as err:
            if settings.ENVIRONMENT.is_debug:
                raise err
            raise ConnectError()

    def get_token(self, port, speed, cals: Connections, upconv: Connections) -> str:
        # Передает токен на основе данных
        if (
            self.token
            and self.port == port
            and self.speed == speed
            and self.cals == self.__to_dict(cals)
            and self.upconv == self.__to_dict(upconv)
        ):
            return self.token
        else:
            return ""

    def is_token_valid(self, token) -> bool:
        return token == self.token

    def apply_attempt(self, port, speed, cals: Connections, upconv: Connections) -> str:
        if not self.__connect(port, speed):
            return False

        # Подключенный к SA cal обязан быть и только 1
        cals_connected_to_sa = [
            cal for cal in cals if MAIN_CAL in cal.connected_to_device
        ]
        if not cals_connected_to_sa:
            raise SANotExistError()

        if len(cals_connected_to_sa) > 1:
            raise ManySADevicesError()

        upconv_connected_to_sa = [
            upconv for upconv in upconv if MAIN_CAL in upconv.connected_to_device
        ]
        if upconv_connected_to_sa:
            raise ConnectedToSAError()

        if self.__check_devices(cals, upconv):
            # Сохраняем последнюю примененную конфигурацию
            self.port = port
            self.speed = speed
            self.token = self.__generate_token(port, speed, self.cals, self.upconv)
            if settings.ENVIRONMENT.is_debug:
                print("\033[93mТокен сгенерирован", self.token, "\033[0m")
            return self.token
        else:
            return ""

    def __check_devices(self, cals: Connections, upconv: Connections) -> bool:
        cals = self.__to_dict(cals)
        upconv = self.__to_dict(upconv)
        try:
            for cal_name, cal_info in cals.items():
                model = cal_info["model_name"]
                if model == "COAXIAL":
                    index = cal_info["index"]
                    command = f"CAL({index})_IDN?"
                    response = self.device.query(command)
                    current_sn = self.__parse_response(response)
                    if current_sn != cal_info["serial_number"]:
                        raise InvalidSerialNumberError(device_name=cal_name)
                elif model == "SMD":
                    pass
                elif model == "SMDvA":
                    raise CalModelSmdvaError()
                else:
                    raise InvalidDeviceModelError()

            for upc_name, upc_info in upconv.items():
                model = upc_info["model_name"]
                if model == "COAXIAL":
                    pass
                elif model == "SMD":
                    pass
                elif model == "SMDvA":
                    index = upc_info["index"]
                    command = f"UpConvA({index})_IDN?"
                    response = self.device.query(command)
                    current_sn = self.__parse_response(response)
                    if current_sn != upc_info["serial_number"]:
                        raise InvalidSerialNumberError(device_name=upc_name)
                else:
                    raise InvalidDeviceModelError()

            # Сохраняем проверенные устройства
            self.cals = cals
            self.upconv = upconv

        except (CalModelSmdvaError, InvalidDeviceModelError) as err:
            raise err
        except Exception:
            raise VisaError()

        return True

    def change_state(
        self,
        device_name: str,
        new_state: str,
        token: str,
    ) -> str:
        # Метод должен принимать attempt_token и проверять его совпадение
        if not self.__connect(self.port, self.speed):
            return False

        access = self.is_token_valid(token)
        if access:
            return self.__change_upconverter_state(device_name, new_state)
        else:
            raise InvalidConncetionError()

    def __change_upconverter_state(
        self, device_name: str, new_state: str
    ) -> str | bool:
        if device_name in self.upconv:
            device = self.upconv[device_name]

            try:
                if device["model_name"] == "COAXIAL":
                    self.device.query(f"SW{device['index']}R")

                if new_state == "CAL":
                    self.device.query(f"UpConvA({device['index']})_CAL")
                    cal_name = device["connected_to_device"]
                    cal_index = self.cals[cal_name]["index"]
                    channel = device["connected_to_device_channel"]
                    command = f"CAL({cal_index})_{channel}"
                    self.device.query(command)
                elif new_state == "CRYO":
                    self.device.query(f"UpConvA({device['index']})_CRYO")
                elif new_state == "TERMINATE":
                    pass
                else:
                    raise InvalidDeviceStateError()

            except Exception:
                raise VisaError()

            device["state_name"] = new_state
            self.token = self.__generate_token(
                self.port, self.speed, self.cals, self.upconv
            )
            return self.token
        else:
            return InvalidDeviceNameError()
