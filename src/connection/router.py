from fastapi import APIRouter, HTTPException

from src.connection.models import *
from src.connection.service import *

router = APIRouter()


@router.put("/connections/{connection_id}", response_model=Connection)
async def update_existing_connection(connection_id: int, updated_connection: ConnectionCreate):
    connection = await read_connection(connection_id)
    if connection:
        return await update_connection(connection_id, updated_connection)
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
