from fastapi import APIRouter, HTTPException

from src.attempt.models import (
    Attempt,
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
    read_last_success_attempt,
    update_attempt,
)
from src.config import device_manager
from src.configuration.service import read_config_connections
from src.port.service import read_port_id
from src.speed.service import read_speed_id

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
        success = device_manager.is_success(
            attempt.port, attempt.speed, config_cals, config_upconv
        )
        return AttemptConnections(
            config_cals=config_cals,
            config_upconv=config_upconv,
            attempt=attempt,
            success=success,
        )
    else:
        raise HTTPException(status_code=404, detail="No attempts found")


@router.get("/last_success", response_model=AttemptConnections)
async def get_last_success_attempt():
    attempt = await read_last_success_attempt()

    if attempt:
        config_cals = await read_config_connections(
            attempt.configuration_id, device_type_name="CAL"
        )
        config_upconv = await read_config_connections(
            attempt.configuration_id, device_type_name="UPCONVERTER"
        )
        success = device_manager.is_success(
            attempt.port, attempt.speed, config_cals, config_upconv
        )
        return AttemptConnections(
            config_cals=config_cals,
            config_upconv=config_upconv,
            attempt=attempt,
            success=success,
        )
    else:
        raise HTTPException(status_code=404, detail="No successful attempts found")


# TODO: Метод должен пытаться применить попытку,
# сначала сохраняя конфигурацию,
# ( Возможно здесь лучше убрать кнопку "Сохранить" на фронте
#  Или поставить на фронте предварительное сохранение )
# после чего запоминая состояние приборов в текущий момент
# после чего пытаться переключить в новое положение считывая из конфигурации
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

    success = device_manager.apply_attempt(
        attempt_related.port, attempt_related.speed, config_cals, config_upconv
    )
    if success:
        return {**attempt, "success": success}
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
