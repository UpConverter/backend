from datetime import datetime

import pytz


def datetime_msc_now() -> str:
    msk_tz = pytz.timezone('Europe/Moscow')
    msc_time = datetime.now(tz=msk_tz)

    return msc_time
