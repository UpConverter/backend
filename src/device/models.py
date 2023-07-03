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


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    type_id: int
    model_id: Optional[int]
    state_id: Optional[int]
    additional_state_id: Optional[int]

    class Config:
        orm_mode = True

class DeviceRelated(DeviceBase):
    type_name: str
    model_name: Optional[str]
    state_name: Optional[str]
    additional_state_name: Optional[str]

class Channel(BaseModel):
    id: int
    name: str
