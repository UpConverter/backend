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


def read_devices_by_type(db: Session, type_name: str, skip: int = 0, limit: int = 100):
    devices_by_type = db.query(schemas.Device).join(schemas.DeviceType).filter(
        schemas.DeviceType.name == type_name
    ).offset(skip).limit(limit).all()
    return devices_by_type


def read_devices_by_types(db: Session, type_names: list[str], skip: int = 0, limit: int = 100):
    devices_by_types = db.query(schemas.Device).join(schemas.DeviceType).filter(
        schemas.DeviceType.name.in_(type_names)
    ).offset(skip).limit(limit).all()

    return devices_by_types


def read_configurations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Configuration).offset(skip).limit(limit).all()
