from sqlalchemy import select, insert, delete, update, func, and_
from src.database import database
from src.attempt import models
from src import schemas
from datetime import datetime


async def read_attempts(skip: int = 0, limit: int = 100):
    select_query = select(schemas.Attempt).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def get_attempt(attempt_id: int):
    select_query = select(schemas.Attempt).where(schemas.Attempt.id == attempt_id)
    return await database.fetch_one(select_query)


async def read_last_success_attempt():
    # Create a subquery to retrieve the maximum timestamp of successful attempts
    subquery = (
        select(func.max(schemas.Attempt.timestamp))
        .where(schemas.Attempt.success)
        .scalar_subquery()
    )

    # Build the main query to fetch the last attempt with success=True
    select_query = select(schemas.Attempt).where(
        and_(
            schemas.Attempt.timestamp == subquery,
            schemas.Attempt.success,
        )
    )
    return await database.fetch_one(select_query)



async def create_attempt(attempt: models.AttemptCreate):
    insert_query = (
        insert(schemas.Attempt)
        .values(
            {
                "configuration_id": attempt.configuration_id,
                "speed_id": attempt.speed_id,
                "port_id": attempt.port_id,
                "success": attempt.success,
                "timestamp": datetime.utcnow(),
            }
        )
    )
    attempt_id = await database.execute(insert_query)

    # Поиск нового значения
    select_query = select(schemas.Attempt).where(
        schemas.Attempt.id == attempt_id
    )
    return await database.fetch_one(select_query)


async def update_attempt(attempt_id: int, attempt: models.AttemptCreate):
    update_query = (
        update(schemas.Attempt)
        .where(schemas.Attempt.id == attempt_id)
        .values(
            configuration_id=attempt.configuration_id,
            speed_id=attempt.speed_id,
            port_id=attempt.port_id,
            success=attempt.success,
            timestamp=datetime.utcnow(),
        )
    )
    await database.execute(update_query)
    return await get_attempt(attempt_id)



async def delete_attempt(attempt_id: int):
    delete_query = (
        delete(schemas.Attempt)
        .where(schemas.Attempt.id == attempt_id)
    )
    
    return await database.execute(delete_query)
