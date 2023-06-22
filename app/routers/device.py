from fastapi import APIRouter, HTTPException, Path, Depends
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..models import DeviceType, DeviceModel, DeviceState, DeviceAdditionalState
from ..crud import read_device_types, read_device_models, read_device_states, read_device_additional_states

router = APIRouter()


@router.get("/device_types", response_model=list[DeviceType])
def get_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_types = read_device_types(db, skip=skip, limit=limit)
    return device_types


@router.get("/device_models", response_model=list[DeviceType])
def get_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_models = read_device_models(db, skip=skip, limit=limit)
    return device_models


@router.get("/device_states", response_model=list[DeviceType])
def get_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_states = read_device_states(db, skip=skip, limit=limit)
    return device_states


@router.get("/device_additional_states", response_model=list[DeviceType])
def get_device_types(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    device_additional_states = read_device_additional_states(
        db, skip=skip, limit=limit)
    return device_additional_states
