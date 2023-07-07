from fastapi import APIRouter

from src.port.models import *
from src.port.service import *

router = APIRouter()


@router.get("/", response_model=list[Port])
async def get_ports(skip: int = 0, limit: int = 100):
    ports = await read_ports(skip=skip, limit=limit)
    return ports
