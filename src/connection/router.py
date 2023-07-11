from fastapi import APIRouter, HTTPException

from src.connection.models import Connection, ConnectionRelatedCreate, ConnectionUpdate
from src.connection.service import delete_connection, read_connection, update_connection
from src.device.service import read_device_channel_id, read_device_id

router = APIRouter()


@router.put("/connections/{connection_id}", response_model=Connection)
async def update_existing_connection(
    connection_id: int, updated_connection: ConnectionRelatedCreate
):
    connection = await read_connection(connection_id)
    if connection:
        device_id = await read_device_id(updated_connection.device)
        connected_to_device_id = await read_device_id(
            updated_connection.connected_to_device
        )
        channel_id = await read_device_channel_id(
            updated_connection.connected_to_device_channel
        )
        return await update_connection(
            connection_id,
            ConnectionUpdate(
                device_id=device_id,
                connected_to_device_id=connected_to_device_id,
                connected_to_device_channel_id=channel_id,
            ),
        )
    else:
        raise HTTPException(status_code=404, detail="Connection not found")


@router.delete("/connections/{connection_id}")
async def delete_existing_connection(connection_id: int):
    connection = await read_connection(connection_id)
    if connection:
        await delete_connection(connection_id)
        return {"message": f"Connection deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Connection not found")
