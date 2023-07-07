from fastapi import APIRouter, HTTPException

from src.attempt.models import Attempt, AttemptCreate, AttemptFull
from src.attempt.service import (
    create_attempt,
    delete_attempt,
    read_attempt,
    read_attempts,
    read_last_success_attempt,
    update_attempt,
)
from src.configuration.service import read_config_connections

router = APIRouter()


@router.get("/", response_model=list[Attempt])
async def get_attempts(skip: int = 0, limit: int = 100):
    attempts = await read_attempts(skip=skip, limit=limit)
    return attempts


@router.get("/last_success", response_model=AttemptFull)
async def get_last_success_attempt():
    attempt = await read_last_success_attempt()
    config_cals = await read_config_connections(
        attempt.configuration_id, device_type_name="CAL"
    )
    config_upconv = await read_config_connections(
        attempt.configuration_id, device_type_name="UPCONVERTER"
    )

    if attempt:
        return {
            "attempt": attempt,
            "config_cals": config_cals,
            "config_upconv": config_upconv,
        }
    else:
        raise HTTPException(status_code=404, detail="No successful attempts found")


# TODO: Метод должен пытаться применить попытку,
# сначала сохраняя конфигурацию,
# ( Возможно здесь лучше убрать кнопку "Сохранить" на фронте
#  Или поставить на фронте предварительное сохранение )
# после чего запоминая состояние приборов в текущий момент
# после чего пытаться переключить в новое положение считывая из конфигурации
@router.post("/", response_model=Attempt)
async def create_new_attempt(attempt: AttemptCreate):
    return await create_attempt(attempt)


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
