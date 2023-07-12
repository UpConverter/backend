from fastapi import APIRouter, HTTPException

from src.connection.models import Connection, ConnectionRelatedCreate, ConnectionUpdate
from src.connection.service import (
    delete_connection,
    read_connection,
    update_connection,
    update_connection_channel,
    update_connection_connected_to,
)
from src.device.service import (
    read_device_channel_id,
    read_device_id,
    read_device_model_id,
)

router = APIRouter()


@router.put("/{connection_id}", response_model=Connection)
async def update_existing_connection(
    connection_id: int, updated_connection: ConnectionRelatedCreate
):
    connection = await read_connection(connection_id)
    if connection:
        connected_to_device_id = await read_device_id(
            updated_connection.connected_to_device
        )
        channel_id = await read_device_channel_id(
            updated_connection.connected_to_device_channel
        )
        model_id = await read_device_model_id(updated_connection.model_name)
        return await update_connection(
            connection_id,
            ConnectionUpdate(
                device_id=updated_connection.device_id,
                model_id=model_id,
                connected_to_device_id=connected_to_device_id,
                connected_to_device_channel_id=channel_id,
            ),
        )
    else:
        raise HTTPException(status_code=404, detail="Connection not found")


@router.put("/{connection_id}/channel", response_model=Connection)
async def update_existing_connection_channel(connection_id: int, channel: str):
    connection = await read_connection(connection_id)
    channel_id = await read_device_channel_id(channel)
    if connection and channel_id:
        return await update_connection_channel(
            connection_id,
            channel_id=channel_id,
        )
    else:
        raise HTTPException(status_code=404, detail="Connection or channel not found")


@router.put("/{connection_id}/connected_to", response_model=Connection)
async def update_existing_connection_connected_to(
    connection_id: int, connected_to: str
):
    connection = await read_connection(connection_id)
    connected_to_id = await read_device_id(connected_to)
    if connection and connected_to_id:
        return await update_connection_connected_to(
            connection_id,
            connected_to_device_id=connected_to_id,
        )

    else:
        raise HTTPException(status_code=404, detail="Connection or channel not found")


@router.delete("/{connection_id}")
async def delete_existing_connection(connection_id: int):
    connection = await read_connection(connection_id)
    if connection:
        await delete_connection(connection_id)
        return {"message": f"Connection deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Connection not found")
