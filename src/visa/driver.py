import pyvisa
from pyvisa.errors import VisaIOError

from src.attempt.constants import MAIN_CAL
from src.connection.models import Connections
from src.visa.exceptions import (
    ConnectedToSAError,
    ConnectError,
    InvalidConncetionError,
    ManySADevicesError,
    SANotExistError,
    UnknownError,
)

PORT_MAPPING = {
    "COM1": "/dev/ttyACM0",
    "COM2": "/dev/ttyACM1",
    "COM3": "/dev/ttyACM2",
    "COM4": "/dev/ttyACM3",
}


class DeviceManager:
    DEVICE_PORT = "ASRL/dev/ttyACM0::INSTR"

    def __init__(self):
        self.rm = pyvisa.ResourceManager()
        self.device = None
        self.port = None
        self.speed = None
        self.cals = []
        self.upconv = []

    def to_dict(self, devices: Connections):
        result = {}
        index = 1

        for device in devices:
            device_dict = {
                "index": index,
                "device_id": device.device_id,
                "model_name": device.model_name,
                "state_name": device.state_name,
                "serial_number": device.serial_number,
                "connected_to_device": device.connected_to_device,
                "connected_to_device_model_name": device.connected_to_device_model_name,
                "connected_to_device_channel": device.connected_to_device_channel,
            }
            result[device.device] = device_dict
            index += 1

        return result

    def connect(self, port, speed) -> bool:
        if self.device and self.port == port and self.speed == speed:
            return True

        try:
            # Если подключен с другими параметрами, то надо будет отключить
            if self.device:
                print("Устройство уже подключено", self.device)
                # self.rm.close()

            port = PORT_MAPPING.get(port)
            self.port = port
            self.speed = speed
            self.device = self.rm.open_resource(port)
            self.device.baud_rate = speed
            return True

        except VisaIOError:
            raise ConnectError()

        except Exception:
            raise UnknownError()

    def is_connected(self) -> bool:
        return self.device

    def is_success(self, port, speed, cals: Connections, upconv: Connections):
        cals = self.to_dict(cals)
        upconv = self.to_dict(upconv)

        return (
            self.port == port
            and self.speed == speed
            and self.cals == cals
            and self.upconv == upconv
        )

    def apply_attempt(
        self, port, speed, cals: Connections, upconv: Connections
    ) -> bool:
        print("\033[93mНеобходимо раскомментировать строчку проверки скорости!\033[0m")
        # if not self.connect(port, speed):
        #     return False

        # Подключенный к SA cal может быть только 1
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

        if self.check_devices(cals, upconv):
            # Сохраняем последнюю примененную конфигурацию
            self.cals = self.to_dict(cals)
            self.upconv = self.to_dict(upconv)
            self.port = port
            self.speed = speed

            return True
        else:
            return False

    def check_devices(self, cals: Connections, upconv: Connections) -> bool:
        all_exist = True
        print(
            "\033[93mНеобходимо добавить логику проверки наличия всех устройств\033[0m"
        )
        #     i = 1
        #     for cal in cals:
        #         f"CAL{i}_IDN?"
        #         # if cal.type_name == ""
        #         try:
        #             visa_instrument.query(f"CAL{i}_IDN?")
        #         except Exception:
        #             all_exist = False
        #             break
        #         i += 1

        #     for upconv in upconv:
        #         try:
        #             visa_instrument.query(f"UPCONV{i}_IDN?")
        #         except Exception:
        #             all_exist = False
        #             break
        #         print()

        return all_exist

    def change_state(
        self,
        device_name: str,
        new_state: str,
        port: str,
        speed: int,
        cals: Connections,
        upconv: Connections,
    ) -> bool:
        success = self.is_success(port, speed, cals, upconv)
        if success:
            return self.__change_upconverter_state(device_name, new_state)
        else:
            raise InvalidConncetionError()

    def __change_upconverter_state(self, device_name: str, new_state: str) -> bool:
        print(
            "\033[93mНеобходимо добавить логику изменения состояния апконвертера\033[0m"
        )
        print("\033[93mDevice name: ", device_name, "New state:", new_state, "\033[0m")
        print("\033[93mSelf.upconv: ", self.upconv[device_name], "\033[0m")
        if device_name in self.upconv:
            device = self.upconv[device_name]
            device["state_name"] = new_state
            return True
        else:
            return False
