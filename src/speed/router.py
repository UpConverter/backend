from fastapi import APIRouter

from src.speed.models import *
from src.speed.service import *

router = APIRouter()


@router.get("/", response_model=list[Speed])
async def get_speeds(skip: int = 0, limit: int = 100):
    speeds = await read_speeds(skip=skip, limit=limit)
    return speeds
