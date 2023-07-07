from sqlalchemy import delete, insert, select, update

from src import schemas
from src.connection import models
from src.database import database


async def get_connection(connection_id: int):
    select_query = select(schemas.Connection).where(
        schemas.Connection.id == connection_id
    )
    return await database.fetch_one(select_query)


async def create_connection(config_id: int, connection: models.ConnectionCreate):
    insert_query = (
        insert(schemas.Connection)
        .values(
            {
                "configuration_id": config_id,
                "device_id": connection.device_id,
                "connected_to_device_id": connection.connected_to_device_id,
                "connected_to_device_channel_id": connection.connected_to_device_channel_id
            }
        )
    )
    connection_id = await database.execute(insert_query)
    return await get_connection(connection_id)


async def update_connection(connection_id: int, connection: models.ConnectionCreate):
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
    return await get_connection(connection_id)


async def delete_connection(connection_id: int):
    delete_query = (
        delete(schemas.Connection)
        .where(schemas.Connection.id == connection_id)
    )

    return await database.execute(delete_query)
