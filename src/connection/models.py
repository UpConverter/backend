from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Configuration(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Connection(BaseModel):
    id: int
    configuration_id: int
    device_id: int
    connected_to_device_id: int
    connected_to_device_channel_id: int


class Connections(BaseModel):
    id: int
    device_id: int
    device_name: str
    model_name: Optional[str]
    connected_to_device_id: Optional[int]
    connected_to_device_channel: Optional[str]

    class Config:
        orm_mode = True

class ConnectionsTyped(Connections):
    type_name: str


class Attempt(BaseModel):
    id: int
    configuration_id: int
    speed_id: int
    port_id: int
    success: bool
    timestamp: datetime
