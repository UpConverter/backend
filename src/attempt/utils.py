from src.attempt.models import AttemptUpconverters
from src.connection.models import Connections


async def group_upconverters_by_cal(
    config_upconv: list[Connections],
) -> list[AttemptUpconverters]:
    grouped_upconverters = {}
    for upconverter in config_upconv:
        cal_name = upconverter.connected_to_device
        if cal_name not in grouped_upconverters:
            grouped_upconverters[cal_name] = []
        grouped_upconverters[cal_name].append(upconverter)

    # Convert the grouped_upconverters dictionary into a list of AttemptUpconverters
    attempt_upconverters_list = []
    for cal_name, upconverters in grouped_upconverters.items():
        attempt_upconverters_list.append(
            AttemptUpconverters(cal=cal_name, upconverters=upconverters)
        )

    return attempt_upconverters_list
