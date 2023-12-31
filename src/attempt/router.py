from fastapi import APIRouter, HTTPException

from src.attempt.models import (
    Attempt,
    AttemptCals,
    AttemptConnections,
    AttemptCreate,
    AttemptRelatedCreate,
    AttemptStatus,
)
from src.attempt.service import (
    create_attempt,
    delete_attempt,
    read_attempt,
    read_attempts,
    read_last_attempt,
    update_attempt,
)
from src.attempt.utils import group_upconverters_by_cal
from src.configuration.service import read_config_connections
from src.port.service import read_port_id
from src.speed.service import read_speed_id
from src.visa.config import device_manager

router = APIRouter()


@router.get("/", response_model=list[Attempt])
async def get_attempts(skip: int = 0, limit: int = 100):
    attempts = await read_attempts(skip=skip, limit=limit)
    return attempts


@router.get("/last", response_model=AttemptConnections)
async def get_last_attempt():
    attempt = await read_last_attempt()

    if attempt:
        config_cals = await read_config_connections(
            attempt.configuration_id, device_type_name="CAL"
        )
        config_upconv = await read_config_connections(
            attempt.configuration_id, device_type_name="UPCONVERTER"
        )
        token = device_manager.get_token(
            attempt.port, attempt.speed, config_cals, config_upconv
        )
        return AttemptConnections(
            config_cals=config_cals,
            config_upconv=config_upconv,
            attempt=attempt,
            attempt_token=token,
        )
    else:
        raise HTTPException(status_code=404, detail="No attempts found")


@router.post("/", response_model=AttemptStatus)
async def create_new_attempt(attempt_related: AttemptRelatedCreate):
    speed_id = await read_speed_id(attempt_related.speed)
    port_id = await read_port_id(attempt_related.port)
    if not speed_id:
        raise HTTPException(status_code=404, detail="Speed not found")
    if not port_id:
        raise HTTPException(status_code=404, detail="Port not found")

    attempt = await create_attempt(
        AttemptCreate(
            configuration_id=attempt_related.configuration_id,
            speed_id=speed_id,
            port_id=port_id,
        ),
    )

    config_cals = await read_config_connections(
        attempt.configuration_id, device_type_name="CAL"
    )
    config_upconv = await read_config_connections(
        attempt.configuration_id, device_type_name="UPCONVERTER"
    )

    token = device_manager.apply_attempt(
        attempt_related.port, attempt_related.speed, config_cals, config_upconv
    )
    if token:
        return {**attempt, "attempt_token": token}
    else:
        raise HTTPException(status_code=403, detail="Ошибка применения конфигурации")


@router.put("/{attempt_id}", response_model=Attempt)
async def update_existing_attempt(attempt_id: int, updated_attempt: AttemptCreate):
    attempt = await read_attempt(attempt_id)
    if attempt:
        return await update_attempt(attempt_id, updated_attempt)
    else:
        raise HTTPException(status_code=404, detail="Attempt not found")


@router.delete("/{attempt_id}")
async def delete_existing_attempt(attempt_id: int):
    attempt = await read_attempt(attempt_id)
    if attempt:
        await delete_attempt(attempt_id)
        return {"message": f"Attempt deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Attempt not found")


@router.get("/last/upconverters", response_model=AttemptCals)
async def get_last_attempt_upconverters():
    attempt = await read_last_attempt()

    if attempt:
        config_cals = await read_config_connections(
            attempt.configuration_id, device_type_name="CAL"
        )
        config_upconv = await read_config_connections(
            attempt.configuration_id, device_type_name="UPCONVERTER"
        )
        token = device_manager.get_token(
            attempt.port, attempt.speed, config_cals, config_upconv
        )
        grouped_cals = await group_upconverters_by_cal(config_upconv)
        return AttemptCals(
            cals=grouped_cals,
            attempt_token=token,
        )
    else:
        raise HTTPException(status_code=404, detail="No attempts found")
