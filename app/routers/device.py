from fastapi import APIRouter, HTTPException, Path, Depends, Query
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..models import Device, DeviceType, DeviceModel, DeviceState, DeviceAdditionalState
from ..crud import read_device_types, read_device_models, read_device_states, read_device_additional_states, read_devices_by_type, read_devices_by_types

router = APIRouter()


@router.get("/device_types", response_model=list[DeviceType])
def get_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_types = read_device_types(db, skip=skip, limit=limit)
    return device_types


@router.get("/device_models", response_model=list[DeviceModel])
def get_device_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_models = read_device_models(db, skip=skip, limit=limit)
    return device_models


@router.get("/device_states", response_model=list[DeviceState])
def get_device_states(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_states = read_device_states(db, skip=skip, limit=limit)
    return device_states


@router.get("/device_additional_states", response_model=list[DeviceAdditionalState])
def get_device_additional_states(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_additional_states = read_device_additional_states(
        db, skip=skip, limit=limit)
    return device_additional_states


@router.get("/devices_by_type", response_model=list[Device])
def get_devices_by_type(type_name: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices_by_type = read_devices_by_type(
        db, type_name, skip=skip, limit=limit)
    return devices_by_type


@router.get("/devices_by_types", response_model=list[Device])
def get_devices_by_types(type_names: list[str] = Query(...), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices_by_types = read_devices_by_types(
        db, type_names, skip=skip, limit=limit)
    return devices_by_types
