from fastapi import APIRouter, HTTPException
from src.attempt.models import AttemptCreate, Attempt
from src.attempt.service import (
    read_attempts,
    get_attempt,
    create_attempt,
    update_attempt,
    delete_attempt,
    read_last_success_attempt,
)

router = APIRouter()


@router.get("/attempts", response_model=list[Attempt])
async def get_attempts(skip: int = 0, limit: int = 100):
    attempts = await read_attempts(skip=skip, limit=limit)
    return attempts


@router.get("/attempts/last_success", response_model=Attempt)
async def get_last_success_attempt():
    attempt = await read_last_success_attempt()
    if attempt:
        return attempt
    else:
        raise HTTPException(
            status_code=404, detail="No successful attempts found")


@router.post("/attempts", response_model=Attempt)
async def create_new_attempt(attempt: AttemptCreate):
    return await create_attempt(attempt)


@router.put("/attempts/{attempt_id}", response_model=Attempt)
async def update_existing_attempt(attempt_id: int, updated_attempt: AttemptCreate):
    attempt = await get_attempt(attempt_id)
    if attempt:
        return await update_attempt(attempt_id, updated_attempt)
    else:
        raise HTTPException(status_code=404, detail="Attempt not found")


@router.delete("/attempts/{attempt_id}")
async def delete_existing_attempt(attempt_id: int):
    attempt = await get_attempt(attempt_id)
    if attempt:
        await delete_attempt(attempt_id)
        return {"message": f"Attempt deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Attempt not found")
