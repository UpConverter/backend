from fastapi import APIRouter
from src.attempt.models import *
from src.attempt.service import *

router = APIRouter()


@router.get("/ports", response_model=list[Port])
async def get_ports(skip: int = 0, limit: int = 100):
    ports = await read_ports(skip=skip, limit=limit)
    return ports


@router.get("/speeds", response_model=list[Speed])
async def get_speeds(skip: int = 0, limit: int = 100):
    speeds = await read_speeds(skip=skip, limit=limit)
    return speeds