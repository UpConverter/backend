from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import aliased

from src import schemas
from src.configuration.models import ConfigurationCreate
from src.connection.models import Connections, ConnectionsTyped
from src.database import database
from src.device.models import DeviceRelated
from src.device.service import read_device_channel_id, read_device_id


async def read_configs():
    select_query = select(schemas.Configuration)
    return await database.fetch_all(select_query)


async def read_config(config_id: int):
    select_query = select(schemas.Configuration).filter(
        schemas.Configuration.id == config_id
    )
    return await database.fetch_one(select_query)


async def create_config(config: ConfigurationCreate):
    insert_query = insert(schemas.Configuration).values(
        {
            "name": config.name,
        }
    )
    config_id = await database.execute(insert_query)

    # Поиск нового значения
    select_query = select(schemas.Configuration).where(
        schemas.Configuration.id == config_id
    )
    return await database.fetch_one(select_query)


async def update_config(config_id: int, configuration: ConfigurationCreate):
    update_query = (
        update(schemas.Configuration)
        .where(
            schemas.Configuration.id == config_id,
        )
        .values(
            name=configuration.name,
        )
    )
    await database.execute(update_query)


async def delete_config(config_id: int):
    async with database.transaction():
        # Удаление всех записей из таблицы connection с указанным configuration_id
        delete_connection_query = delete(schemas.Connection).where(
            schemas.Connection.configuration_id == config_id
        )
        await database.execute(delete_connection_query)

        # Удаление самой конфигурации
        delete_configuration_query = delete(schemas.Configuration).where(
            schemas.Configuration.id == config_id
        )
        await database.execute(delete_configuration_query)


async def read_config_connections(
    config_id: int, device_type_name: str = None
) -> Connections:
    main_device = aliased(schemas.Device)
    connected_device = aliased(schemas.Device)

    select_query = (
        select(
            schemas.Connection.id,
            main_device.name.label("device"),
            schemas.DeviceModel.name.label("model_name"),
            schemas.DeviceType.name.label("type_name"),
            schemas.DeviceState.name.label("state_name"),
            connected_device.name.label("connected_to_device"),
            schemas.Channel.name.label("connected_to_device_channel"),
        )
        .select_from(schemas.Connection)
        .join(main_device, schemas.Connection.device_id == main_device.id)
        .join(schemas.DeviceModel, main_device.model_id == schemas.DeviceModel.id)
        .join(schemas.DeviceType, main_device.type_id == schemas.DeviceType.id)
        .outerjoin(schemas.DeviceState, main_device.state_id == schemas.DeviceState.id)
        .join(
            connected_device,
            schemas.Connection.connected_to_device_id == connected_device.id,
        )
        .join(
            schemas.Channel,
            schemas.Connection.connected_to_device_channel_id == schemas.Channel.id,
        )
        .filter(schemas.Connection.configuration_id == config_id)
    )

    if device_type_name:
        select_query = select_query.filter(schemas.DeviceType.name == device_type_name)

    result = await database.fetch_all(select_query)

    return result


async def read_config_avaliable_devices(
    config_id: int, type_name: str
) -> list[DeviceRelated]:
    # Получение идентификаторов устройств из таблицы connections для указанной конфигурации
    connection_devices = select([schemas.Connection.device_id]).where(
        schemas.Connection.configuration_id == config_id
    )

    # Получение всех устройств заданного типа, исключая устройства из таблицы connections
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
        .filter(schemas.DeviceType.name == type_name)
        .filter(~schemas.Device.id.in_(connection_devices))
    )

    devices = await database.fetch_all(select_query)
    return devices


async def update_config_connections(config_id: int, connections: ConnectionsTyped):
    async with database.transaction():
        # Обновление Connections для config_cals
        for connection in connections.config_cals:
            await update_config_connection(config_id, connection)

        # Обновление Connections для config_upconv
        for connection in connections.config_upconv:
            await update_config_connection(config_id, connection)


# TODO: Добавить изменение сущности устройства
async def update_config_connection(config_id: int, connection: Connections):
    connection.device_id = await read_device_id(connection.device_name)
    connection.connected_to_device_id = await read_device_id(
        connection.connected_to_device
    )
    connection.connected_to_device_channel_id = await read_device_channel_id(
        connection.connected_to_device_channel
    )

    update_query = (
        update(schemas.Connection)
        .where(
            schemas.Connection.configuration_id == config_id,
            schemas.Connection.id == connection.id,
        )
        .values(
            device_id=connection.device_id,
            connected_to_device_id=connection.connected_to_device_id,
            connected_to_device_channel_id=connection.connected_to_device_channel_id,
        )
    )
    await database.execute(update_query)
