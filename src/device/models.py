from pydantic import BaseModel
from typing import Optional


class DeviceType(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DeviceModel(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DeviceState(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DeviceAdditionalState(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    id: int
    serial_number: int
    type_id: int
    model_id: Optional[int]
    state_id: Optional[int]
    additional_state_id: Optional[int]


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    class Config:
        orm_mode = True


class Channel(BaseModel):
    id: int
    name: str
