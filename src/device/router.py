from fastapi import APIRouter, HTTPException, Query

from src.device.models import *
from src.device.service import *

router = APIRouter()


@router.get("/types", response_model=list[DeviceType])
async def get_device_types(skip: int = 0, limit: int = 100):
    device_types = await read_device_types(skip=skip, limit=limit)
    return device_types


@router.get("/models", response_model=list[DeviceModel])
async def get_device_models(skip: int = 0, limit: int = 100):
    device_models = await read_device_models(skip=skip, limit=limit)
    return device_models


@router.get("/states", response_model=list[DeviceState])
async def get_device_states(skip: int = 0, limit: int = 100):
    device_states = await read_device_states(skip=skip, limit=limit)
    return device_states


@router.get("/additional_states", response_model=list[DeviceAdditionalState])
async def get_device_additional_states(skip: int = 0, limit: int = 100):
    device_additional_states = await read_device_additional_states(
        skip=skip, limit=limit)
    return device_additional_states


@router.get("/channels", response_model=list[DeviceAdditionalState])
async def get_device_additional_states(skip: int = 0, limit: int = 100):
    device_channels = await read_device_channels(
        skip=skip, limit=limit)
    return device_channels


@router.get("/by_type", response_model=list[Device])
async def get_devices_by_type(type_name: str, skip: int = 0, limit: int = 100):
    devices_by_type = await read_devices_by_type(
        type_name, skip=skip, limit=limit)
    return devices_by_type


@router.get("/by_types", response_model=list[Device])
async def get_devices_by_types(type_names: list[str] = Query(...), skip: int = 0, limit: int = 100):
    devices_by_types = await read_devices_by_types(
        type_names, skip=skip, limit=limit)
    return devices_by_types


@router.get("/by_types_related", response_model=list[DeviceRelated])
async def get_devices_by_types_related(type_names: list[str] = Query(...), skip: int = 0, limit: int = 100):
    devices_by_types = await read_devices_by_types_related(
        type_names, skip=skip, limit=limit)
    if devices_by_types:
        return devices_by_types
    else:
        raise HTTPException(status_code=404, detail="Devices not found")


@router.get("/{device_id}", response_model=DeviceRelated)
async def get_device(device_id: int):
    device = await read_device_related(device_id)
    if device:
        return device
    else:
        raise HTTPException(status_code=404, detail="Device not found")


@router.post("/", response_model=Device)
async def create_new_device(device: DeviceRelatedCreate):
    exist_device = await read_device_id(device.name)
    if exist_device:
        raise HTTPException(
            status_code=404, detail=f"Device with name {device.name} already exist")
    else:
        return await create_device(device)


@router.put("/{device_id}", response_model=Device)
async def update_existing_device(device_id: int, updated_device: DeviceRelatedCreate):
    device = await read_device(device_id)
    if device:
        return await update_device(device_id, updated_device)
    else:
        raise HTTPException(status_code=404, detail="Device not found")


@router.delete("/{device_id}")
async def delete_existing_device(device_id: int):
    device = await read_device(device_id)
    if device:
        await delete_device(device_id)
        return {"message": f"Device deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Device not found")
