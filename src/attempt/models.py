from pydantic import BaseModel
from datetime import datetime


class Port(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Speed(BaseModel):
    id: int
    value: int

    class Config:
        orm_mode = True


class AttemptBase(BaseModel):
    id: int
    configuration_id: int
    speed_id: int
    port_id: int
    success: bool
    timestamp: datetime


class AttemptCreate(AttemptBase):
    pass


class Attempt(AttemptBase):
    class Config:
        orm_mode = True
