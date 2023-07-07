from sqlalchemy import select

from src import schemas
from src.database import database


async def read_speeds(skip: int = 0, limit: int = 100):
    select_query = select(schemas.Speed).offset(skip).limit(limit)
    return await database.fetch_all(select_query)
