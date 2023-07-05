from sqlalchemy import select
from src import schemas
from src.database import database


async def read_device_types(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceType).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def get_device_type_id(type_name: str) -> int:
    query = select(schemas.DeviceType.id).where(
        schemas.DeviceType.name == type_name).limit(1)
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_models(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceModel).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def get_device_model_id(model_name: str) -> int:
    query = select(schemas.DeviceModel.id).where(
        schemas.DeviceModel.name == model_name).limit(1)
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_states(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceState).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def get_device_state_id(state_name: str) -> int:
    query = select(schemas.DeviceState.id).where(
        schemas.DeviceState.name == state_name).limit(1)
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_additional_states(skip: int = 0, limit: int = 100):
    select_query = select(
        schemas.DeviceAdditionalState).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_device_channels(skip: int = 0, limit: int = 100):
    select_query = select(schemas.Channel).offset(skip).limit(limit)
    return await database.fetch_all(select_query)

# TODO: Добавить обработку ошибки


async def get_device_channel_id(channel_name: str) -> int:
    query = select(schemas.Channel.id).where(
        schemas.Channel.name == channel_name).limit(1)
    result = await database.fetch_one(query)
    return result.id if result else None


# TODO: Добавить обработку ошибки
async def get_device_id(device_name: str) -> int:
    query = select(schemas.Device.id).where(
        schemas.Device.name == device_name).limit(1)
    result = await database.fetch_one(query)
    return result.device_id if result else None


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


async def read_device(device_id: int):
    select_query = (
        select(
            schemas.Device,
            schemas.DeviceType.name.label("type_name"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceState.name.label("state_name"),
            schemas.DeviceAdditionalState.name.label("additional_state_name")
        )
        .join(schemas.DeviceType)
        .outerjoin(schemas.DeviceState)
        .outerjoin(schemas.DeviceModel)
        .outerjoin(schemas.DeviceAdditionalState)
        .filter(schemas.Device.id == device_id)
    )
    device = await database.fetch_one(select_query)
    return device


async def read_devices_by_types_related(type_names: list[str], skip: int = 0, limit: int = 100):
    select_query = (
        select(
            schemas.Device,
            schemas.DeviceType.name.label("type_name"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceState.name.label("state_name"),
            schemas.DeviceAdditionalState.name.label("additional_state_name")
        )
        .join(schemas.Device.type_)
        .outerjoin(schemas.Device.state)
        .outerjoin(schemas.DeviceModel)
        .outerjoin(schemas.Device.additional_state)
        .filter(
            schemas.DeviceType.name.in_(type_names)
        )
        .offset(skip).limit(limit)
    )
    device = await database.fetch_all(select_query)
    return device
