from sqlalchemy import select
from sqlalchemy.orm import aliased
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
async def read_config_connections(config_id: int, device_type_name: str = None):
    main_device = aliased(schemas.Device)
    connected_device = aliased(schemas.Device)

    select_query = (
        select(
            schemas.Connection.id,
            schemas.Connection.device_id,
            main_device.name.label("device_name"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceType.name.label("type_name"),
            schemas.DeviceState.name.label("state_name"),
            schemas.Connection.connected_to_device_id,
            connected_device.name.label("connected_to_device_name"),
            schemas.Channel.name.label("connected_to_device_channel")
        )
        .select_from(schemas.Connection)
        .join(main_device, schemas.Connection.device_id == main_device.id)
        .join(schemas.DeviceModel, main_device.model_id == schemas.DeviceModel.id)
        .join(schemas.DeviceType, main_device.type_id == schemas.DeviceType.id)
        .outerjoin(schemas.DeviceState, main_device.state_id == schemas.DeviceState.id)
        .join(connected_device, schemas.Connection.connected_to_device_id == connected_device.id)
        .join(schemas.Channel, schemas.Connection.connected_to_device_channel_id == schemas.Channel.id)
        .filter(schemas.Connection.configuration_id == config_id)
    )

    if device_type_name:
        select_query = select_query.filter(
            schemas.DeviceType.name == device_type_name)

    result = await database.fetch_all(select_query)

    return result
