from sqlalchemy import select

from src import schemas
from src.database import database


async def read_ports(skip: int = 0, limit: int = 100):
    select_query = select(schemas.Port).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_port_id(port: str) -> int:
    query = select(schemas.Port.id).where(schemas.Port.name == port).limit(1)
    result = await database.fetch_one(query)
    return result.id if result else None
