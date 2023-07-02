from fastapi import APIRouter, Query
from src.device.models import *
from src.device.service import *

router = APIRouter()


@router.get("/device_types", response_model=list[DeviceType])
async def get_device_types(skip: int = 0, limit: int = 100):
    device_types = await read_device_types(skip=skip, limit=limit)
    return device_types


@router.get("/device_models", response_model=list[DeviceModel])
async def get_device_models(skip: int = 0, limit: int = 100):
    device_models = await read_device_models(skip=skip, limit=limit)
    return device_models


@router.get("/device_states", response_model=list[DeviceState])
async def get_device_states(skip: int = 0, limit: int = 100):
    device_states = await read_device_states(skip=skip, limit=limit)
    return device_states


@router.get("/device_additional_states", response_model=list[DeviceAdditionalState])
async def get_device_additional_states(skip: int = 0, limit: int = 100):
    device_additional_states = await read_device_additional_states(
        skip=skip, limit=limit)
    return device_additional_states


@router.get("/devices_by_type", response_model=list[Device])
async def get_devices_by_type(type_name: str, skip: int = 0, limit: int = 100):
    devices_by_type = await read_devices_by_type(
        type_name, skip=skip, limit=limit)
    return devices_by_type


@router.get("/devices_by_types", response_model=list[Device])
async def get_devices_by_types(type_names: list[str] = Query(...), skip: int = 0, limit: int = 100):
    devices_by_types = await read_devices_by_types(
        type_names, skip=skip, limit=limit)
    return devices_by_types
