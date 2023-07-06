from src.connection.models import Connections
from src.attempt.constants import MAIN_CAL
import pyvisa

def apply_attempt(cals: Connections, upconv: Connections) -> bool:
    success = True
    main_cal = [cal for cal in cals if MAIN_CAL in cal.connected_to_device]

    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

    if not main_cal:
        success = False

    return success