from sqlalchemy import select
from src import schemas
from src.database import database


async def read_device_types(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceType).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_device_models(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceModel).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_device_states(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceState).offset(skip).limit(limit)
    result = await database.fetch_all(select_query)
    print(result)
    return result


async def read_device_additional_states(skip: int = 0, limit: int = 100):
    select_query = select(
        schemas.DeviceAdditionalState).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_devices_by_type(type_name: str, skip: int = 0, limit: int = 100):
    select_query = select(schemas.Device).join(schemas.DeviceType).filter(
        schemas.DeviceType.name == type_name
    ).offset(skip).limit(limit)
    devices_by_type = await database.fetch_all(select_query)
    return devices_by_type


async def read_devices_by_types(type_names: list[str], skip: int = 0, limit: int = 100):
    select_query = select(schemas.Device).join(schemas.DeviceType).filter(
        schemas.DeviceType.name.in_(type_names)
    ).offset(skip).limit(limit)
    devices_by_types = await database.fetch_all(select_query)
    return devices_by_types
