from sqlalchemy import select
from src import schemas
from src.database import database


async def read_configs():
    select_query = (
        select(
            schemas.Configuration
        )
    )
    return await database.fetch_all(select_query)


async def read_config(config_id: int):
    select_query = (
        select(
            schemas.Configuration
        )
        .filter(schemas.Configuration.id == config_id)
    )
    return await database.fetch_one(select_query)


# { device_id: 1, model_name: 'Coaxial', connected_to_device_id: 0, connected_to_device_channel: 'SW1' },
async def read_config_connections(config_id: int, device_type_names: list[str] = None):
    select_query = (
        select(
            schemas.Connection.id,
            schemas.Connection.device_id,
            schemas.Device.name.label("device_name"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceType.name.label("type_name"),
            schemas.Connection.connected_to_device_id,
            schemas.Channel.name.label("connected_to_device_channel")
        )
        .join(schemas.Device, schemas.Connection.device_id == schemas.Device.id)
        .join(schemas.DeviceModel, schemas.Device.model_id == schemas.DeviceModel.id)
        .join(schemas.DeviceType, schemas.Device.type_id == schemas.DeviceType.id)
        .join(schemas.Channel, schemas.Connection.connected_to_device_channel_id == schemas.Channel.id)
        .filter(schemas.Connection.configuration_id == config_id)
    )

    if device_type_names:
        select_query = select_query.filter(
            schemas.DeviceType.name.in_(device_type_names))

    result = await database.fetch_all(select_query)

    return result
