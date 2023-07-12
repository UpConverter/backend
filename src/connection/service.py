from sqlalchemy import delete, insert, select, update

from src import schemas
from src.connection import models
from src.database import database
from src.device.service import read_device_main_channel, read_main_device


async def read_connection(connection_id: int):
    select_query = select(schemas.Connection).where(
        schemas.Connection.id == connection_id
    )
    return await database.fetch_one(select_query)


async def create_connection(config_id: int, connection: models.ConnectionCreate):
    main_device = await read_main_device()
    main_channel = await read_device_main_channel()

    insert_query = insert(schemas.Connection).values(
        {
            "configuration_id": config_id,
            "device_id": connection.device_id,
            "connected_to_device_id": main_device.id,
            "connected_to_device_channel_id": main_channel.id,
        }
    )
    connection_id = await database.execute(insert_query)
    return await read_connection(connection_id)


async def update_connection(connection_id: int, connection: models.ConnectionUpdate):
    update_query = (
        update(schemas.Connection)
        .where(schemas.Connection.id == connection_id)
        .values(
            device_id=connection.device_id,
            connected_to_device_id=connection.connected_to_device_id,
            connected_to_device_channel_id=connection.connected_to_device_channel_id,
        )
    )
    await database.execute(update_query)
    return await read_connection(connection_id)


async def update_connection_channel(connection_id: int, channel_id: int):
    update_query = (
        update(schemas.Connection)
        .where(schemas.Connection.id == connection_id)
        .values(
            connected_to_device_channel_id=channel_id,
        )
    )
    await database.execute(update_query)
    return await read_connection(connection_id)


async def update_connection_connected_to(
    connection_id: int, connected_to_device_id: int
):
    update_query = (
        update(schemas.Connection)
        .where(schemas.Connection.id == connection_id)
        .values(
            connected_to_device_id=connected_to_device_id,
        )
    )
    await database.execute(update_query)
    return await read_connection(connection_id)


async def delete_connection(connection_id: int):
    delete_query = delete(schemas.Connection).where(
        schemas.Connection.id == connection_id
    )

    return await database.execute(delete_query)
