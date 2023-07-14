from sqlalchemy import select

from src import schemas
from src.database import database


async def gen_unique_serial_number() -> int:
    select_query = select(schemas.Device.serial_number)
    serials = await database.fetch_all(select_query)

    if serials:
        unique_serials = [row[0] for row in serials]
        unique_serial = max(unique_serials) + 1
    else:
        unique_serial = 1000000

    return unique_serial


async def is_unique_serial_number(serial_number) -> bool:
    select_query = select(schemas.Device.serial_number)
    serials = await database.fetch_all(select_query)
    unique_serials = [row[0] for row in serials]

    return serial_number not in unique_serials
