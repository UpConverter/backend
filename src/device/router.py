from fastapi import APIRouter, HTTPException, Query

from src.device.models import *
from src.device.service import *
from src.device.utils import is_unique_serial_number
from src.visa.config import device_manager
from src.visa.exceptions import StateChangeError

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
        skip=skip, limit=limit
    )
    return device_additional_states


@router.get("/channels", response_model=list[DeviceChannel])
async def get_device_channels(skip: int = 0, limit: int = 100):
    device_channels = await read_device_channels(skip=skip, limit=limit)
    return device_channels


@router.get("/by_type", response_model=list[Device])
async def get_devices_by_type(type_name: str, skip: int = 0, limit: int = 100):
    devices_by_type = await read_devices_by_type(type_name, skip=skip, limit=limit)
    return devices_by_type


@router.get("/by_types", response_model=list[Device])
async def get_devices_by_types(
    type_names: list[str] = Query(...), skip: int = 0, limit: int = 100
):
    devices_by_types = await read_devices_by_types(type_names, skip=skip, limit=limit)
    return devices_by_types


@router.get("/by_type_related", response_model=list[DeviceRelated])
async def get_devices_by_type_related(type_name: str, skip: int = 0, limit: int = 100):
    devices_by_types = await read_devices_by_type_related(
        type_name, skip=skip, limit=limit
    )
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


@router.post("/cal", response_model=Device)
async def create_new_cal(device: CalCreate):
    exist_device = await read_device_id(device.name)
    if exist_device:
        raise HTTPException(
            status_code=404, detail=f"Device with name {device.name} already exist"
        )
    else:
        return await create_cal(device)


@router.post("/", response_model=Device)
async def create_new_device(device: DeviceRelatedCreate):
    exist_device = await read_device_id(device.name)
    if exist_device:
        raise HTTPException(
            status_code=409, detail=f"Device with name {device.name} already exist"
        )
    if await is_unique_serial_number(device.serial_number):
        return await create_device(device)
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Device with serial number {device.serial_number} already exist",
        )


@router.put("/{device_id}", response_model=Device)
async def update_existing_device(device_id: int, updated_device: DeviceRelatedCreate):
    device = await read_device(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    if updated_device.serial_number == device.serial_number:
        return await update_device(device_id, updated_device)

    if await is_unique_serial_number(updated_device.serial_number):
        return await update_device(device_id, updated_device)
    else:
        raise HTTPException(
            status_code=409,
            detail=f"Device with serial number {device.serial_number} already exist",
        )


@router.delete("/{device_id}")
async def delete_existing_device(device_id: int):
    device = await read_device(device_id)
    if device:
        await delete_device(device_id)
        return {"message": f"Device deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Device not found")


@router.put("/{device_id}/model", response_model=Device)
async def update_existing_device_model(device_id: int, model: str):
    device = await read_device(device_id)
    if device:
        model_id = await read_device_model_id(model)
        return await update_device_model(device_id, model_id)
    else:
        raise HTTPException(status_code=404, detail="Device not found")


@router.put("/{device_id}/state")
async def update_existing_device_state(
    device_id: int, new_state: str, attempt_token: str
):
    exist_device = await read_device(device_id)
    if not exist_device:
        raise HTTPException(status_code=404, detail="Device not found")

    state_id = await read_device_state_id(new_state)
    if not state_id:
        raise HTTPException(status_code=404, detail="State id not found")

    new_token = device_manager.change_state(exist_device.name, new_state, attempt_token)
    if new_token:
        await update_device_state(device_id, state_id)
        return {"attempt_token": new_token}
    else:
        raise StateChangeError()
