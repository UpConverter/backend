from sqlalchemy.orm import Session
from . import models, schemas


def read_ports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Port).offset(skip).limit(limit).all()


def read_channels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Channel).offset(skip).limit(limit).all()


def read_speeds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Speed).offset(skip).limit(limit).all()


def read_device_types(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.DeviceType).offset(skip).limit(limit).all()


def read_device_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.DeviceModel).offset(skip).limit(limit).all()


def read_device_states(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.DeviceState).offset(skip).limit(limit).all()


def read_device_additional_states(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.DeviceAdditionalState).offset(skip).limit(limit).all()
