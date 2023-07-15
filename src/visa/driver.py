import pyvisa
from pyvisa.errors import VisaIOError

from src.attempt.constants import MAIN_CAL
from src.connection.models import Connections
from src.visa.exceptions import (
    ConnectedToSAError,
    ConnectError,
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
        cals = [cal.device for cal in cals]
        upconv = [up.device for up in upconv]
        return (
            self.port == port
            and self.speed == speed
            and self.cals == cals
            and self.upconv == upconv
        )

    def apply_attempt(
        self, port, speed, cals: Connections, upconv: Connections
    ) -> bool:
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

        # Сохраняем последнюю примененную конфигурацию
        self.cals = [cal.device for cal in cals]
        self.upconv = [up.device for up in upconv]
        self.port = port
        self.speed = speed

        return True

    # def check_devices(cals: Connections, upconv: Connections, visa_instrument) -> bool:
    #     all_exist = True
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

    #     return all_exist
