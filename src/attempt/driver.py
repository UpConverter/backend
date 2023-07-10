import pyvisa
from pyvisa.errors import VisaIOError

from src.attempt.constants import MAIN_CAL
from src.connection.models import Connections

DEVICE_PORT = "ASRL/dev/ttyACM0::INSTR"


def apply_attempt(cals: Connections, upconv: Connections) -> bool:
    success = True
    main_cal = [cal for cal in cals if MAIN_CAL in cal.connected_to_device]

    try:
        rm = pyvisa.ResourceManager()
        print(rm.list_resources())
        my_instrument = rm.open_resource(DEVICE_PORT)
        my_instrument.read_termination = "\r\n"
        my_instrument.write_termination = "\r\n"
        my_instrument.baud_rate = 115200
        print(my_instrument.query("CAL(1)_CH1"))
    except VisaIOError as err:
        print(f"An error occurred during instrument communication: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    if not main_cal:
        success = False

    return success
