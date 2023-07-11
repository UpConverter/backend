from sqlalchemy import delete, insert, select, update

from src import schemas
from src.database import database
from src.device import models
from src.device.models import Device, DeviceChannel
from src.device.utils import gen_unique_serial_number


async def read_device_types(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceType).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def read_device_type_id(type_name: str) -> int:
    query = (
        select(schemas.DeviceType.id)
        .where(schemas.DeviceType.name == type_name)
        .limit(1)
    )
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_models(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceModel).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def read_device_model_id(model_name: str) -> int:
    query = (
        select(schemas.DeviceModel.id)
        .where(schemas.DeviceModel.name == model_name)
        .limit(1)
    )
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_states(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceState).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def read_device_state_id(state_name: str) -> int:
    query = (
        select(schemas.DeviceState.id)
        .where(schemas.DeviceState.name == state_name)
        .limit(1)
    )
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_additional_states(skip: int = 0, limit: int = 100):
    select_query = select(schemas.DeviceAdditionalState).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


# TODO: Добавить обработку ошибки
async def read_device_additional_state_id(additional_state_name: str) -> int:
    query = (
        select(schemas.DeviceAdditionalState.id)
        .where(schemas.DeviceAdditionalState.name == additional_state_name)
        .limit(1)
    )
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_device_channels(skip: int = 0, limit: int = 100):
    select_query = select(schemas.Channel).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_device_main_channel() -> DeviceChannel:
    select_query = select(schemas.Channel)
    return await database.fetch_one(select_query)


# TODO: Добавить обработку ошибки
async def read_device_channel_id(channel_name: str) -> int:
    query = (
        select(schemas.Channel.id).where(schemas.Channel.name == channel_name).limit(1)
    )
    result = await database.fetch_one(query)
    return result.id if result else None


async def read_main_device(type_name="SA") -> Device:
    select_query = (
        select(schemas.Device)
        .join(schemas.DeviceType)
        .filter(schemas.DeviceType.name == type_name)
    )
    device = await database.fetch_one(select_query)
    return device


async def read_device(device_id: int):
    select_query = select(schemas.Device).filter(schemas.Device.id == device_id)
    return await database.fetch_one(select_query)


# TODO: Добавить обработку ошибки
async def read_device_id(device_name: str) -> int:
    query = select(schemas.Device.id).where(schemas.Device.name == device_name).limit(1)
    result = await database.fetch_one(query)
    return result.id if result else None


async def create_device(device: models.DeviceRelatedCreate):
    serial_number = await gen_unique_serial_number()
    type_id = await read_device_type_id(device.type_name)
    model_id = await read_device_model_id(device.model_name)
    state_id = await read_device_state_id(device.state_name)
    additional_state_id = await read_device_additional_state_id(
        device.additional_state_name
    )

    insert_query = insert(schemas.Device).values(
        {
            "name": device.name,
            "serial_number": serial_number,
            "type_id": type_id,
            "model_id": model_id,
            "state_id": state_id,
            "additional_state_id": additional_state_id,
        }
    )
    device_id = await database.execute(insert_query)
    return await read_device(device_id)


async def update_device(device_id: int, device: models.DeviceRelatedCreate):
    update_values = {
        "name": device.name,
    }

    if device.type_name:
        type_id = await read_device_type_id(device.type_name)
        update_values["type_id"] = type_id

    if device.model_name:
        model_id = await read_device_model_id(device.model_name)
        update_values["model_id"] = model_id

    if device.state_name:
        state_id = await read_device_state_id(device.state_name)
        update_values["state_id"] = state_id

    if device.additional_state_name:
        additional_state_id = await read_device_additional_state_id(
            device.additional_state_name
        )
        update_values["additional_state_id"] = additional_state_id

    update_query = (
        update(schemas.Device)
        .where(schemas.Device.id == device_id)
        .values(**update_values)
    )
    await database.execute(update_query)
    return await read_device(device_id)


async def delete_device(device_id: int):
    delete_query = delete(schemas.Device).where(schemas.Device.id == device_id)

    return await database.execute(delete_query)


async def read_devices_by_type(type_name: str, skip: int = 0, limit: int = 100):
    select_query = (
        select(schemas.Device)
        .join(schemas.DeviceType)
        .filter(schemas.DeviceType.name == type_name)
        .offset(skip)
        .limit(limit)
    )
    devices_by_type = await database.fetch_all(select_query)
    return devices_by_type


async def read_devices_by_types(type_names: list[str], skip: int = 0, limit: int = 100):
    select_query = (
        select(schemas.Device)
        .join(schemas.DeviceType)
        .filter(schemas.DeviceType.name.in_(type_names))
        .offset(skip)
        .limit(limit)
    )
    devices_by_types = await database.fetch_all(select_query)
    return devices_by_types


async def read_device_related(device_id: int):
    select_query = (
        select(
            schemas.Device,
            schemas.DeviceType.name.label("type_name"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceState.name.label("state_name"),
            schemas.DeviceAdditionalState.name.label("additional_state_name"),
        )
        .join(schemas.DeviceType)
        .outerjoin(schemas.DeviceState)
        .outerjoin(schemas.DeviceModel)
        .outerjoin(schemas.DeviceAdditionalState)
        .filter(schemas.Device.id == device_id)
    )
    device = await database.fetch_one(select_query)
    return device


async def read_devices_by_types_related(
    type_names: list[str], skip: int = 0, limit: int = 100
):
    select_query = (
        select(
            schemas.Device,
            schemas.DeviceType.name.label("type_name"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceState.name.label("state_name"),
            schemas.DeviceAdditionalState.name.label("additional_state_name"),
        )
        .join(schemas.Device.type_)
        .outerjoin(schemas.Device.state)
        .outerjoin(schemas.DeviceModel)
        .outerjoin(schemas.Device.additional_state)
        .filter(schemas.DeviceType.name.in_(type_names))
        .offset(skip)
        .limit(limit)
    )
    device = await database.fetch_all(select_query)
    return device
