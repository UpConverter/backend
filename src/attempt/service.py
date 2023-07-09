from datetime import datetime

from sqlalchemy import and_, delete, func, insert, select, update

from src import schemas
from src.attempt import models
from src.attempt.driver import apply_attempt
from src.configuration.service import read_config_connections
from src.database import database
from src.utils import datetime_msc_now


async def read_attempts(skip: int = 0, limit: int = 100):
    select_query = select(schemas.Attempt).offset(skip).limit(limit)
    return await database.fetch_all(select_query)


async def read_attempt(attempt_id: int):
    select_query = select(schemas.Attempt).where(schemas.Attempt.id == attempt_id)
    return await database.fetch_one(select_query)


async def create_attempt(attempt: models.AttemptCreate) -> models.Attempt:
    config_cals = await read_config_connections(
        attempt.configuration_id, device_type_name="CAL"
    )
    config_upconv = await read_config_connections(
        attempt.configuration_id, device_type_name="UPCONVERTER"
    )
    success = apply_attempt(config_cals, config_upconv)

    insert_query = insert(schemas.Attempt).values(
        {
            "configuration_id": attempt.configuration_id,
            "speed_id": attempt.speed_id,
            "port_id": attempt.port_id,
            "success": success,
            "timestamp": datetime_msc_now(),
        }
    )
    attempt_id = await database.execute(insert_query)

    # Поиск нового значения
    select_query = select(schemas.Attempt).where(schemas.Attempt.id == attempt_id)
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
    return await read_attempt(attempt_id)


async def delete_attempt(attempt_id: int):
    delete_query = delete(schemas.Attempt).where(schemas.Attempt.id == attempt_id)

    return await database.execute(delete_query)


async def read_last_attempt():
    subquery = select(func.max(schemas.Attempt.timestamp)).scalar_subquery()

    select_query = (
        select(
            schemas.Attempt.success,
            schemas.Configuration.id.label("configuration_id"),
            schemas.Configuration.name.label("configuration"),
            schemas.Speed.value.label("speed"),
            schemas.Port.name.label("port"),
        )
        .where(
            schemas.Attempt.timestamp == subquery,
        )
        .join(
            schemas.Configuration,
            schemas.Attempt.configuration_id == schemas.Configuration.id,
        )
        .join(
            schemas.Speed,
            schemas.Attempt.speed_id == schemas.Speed.id,
        )
        .join(
            schemas.Port,
            schemas.Attempt.port_id == schemas.Port.id,
        )
    )

    result = await database.fetch_one(select_query)

    return result


async def read_last_success_attempt():
    # Create a subquery to retrieve the maximum timestamp of successful attempts
    subquery = (
        select(func.max(schemas.Attempt.timestamp))
        .where(schemas.Attempt.success)
        .scalar_subquery()
    )

    # Build the main query to fetch the last attempt with success=True
    select_query = (
        select(
            schemas.Attempt.success,
            schemas.Configuration.id.label("configuration_id"),
            schemas.Configuration.name.label("configuration"),
            schemas.Speed.value.label("speed"),
            schemas.Port.name.label("port"),
        )
        .where(
            and_(
                schemas.Attempt.timestamp == subquery,
                schemas.Attempt.success,
            )
        )
        .join(
            schemas.Configuration,
            schemas.Attempt.configuration_id == schemas.Configuration.id,
        )
        .join(
            schemas.Speed,
            schemas.Attempt.speed_id == schemas.Speed.id,
        )
        .join(
            schemas.Port,
            schemas.Attempt.port_id == schemas.Port.id,
        )
    )

    result = await database.fetch_one(select_query)

    return result
