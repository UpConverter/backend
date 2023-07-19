from typing import Optional

from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    device_id: int


class ConnectionUpdate(ConnectionCreate):
    connected_to_device_id: Optional[int]
    connected_to_device_channel_id: Optional[int]


class Connection(ConnectionUpdate):
    id: int
    configuration_id: int


class ConnectionRelatedCreate(BaseModel):
    device_id: int
    device: str
    connected_to_device: Optional[str]
    connected_to_device_model_name: Optional[str]
    connected_to_device_channel: Optional[str]


class Connections(ConnectionRelatedCreate):
    id: int
    serial_number: str
    model_name: Optional[str]
    state_name: Optional[str]
    additional_state_name: Optional[str]

    class Config:
        orm_mode = True


class ConnectionsTyped(BaseModel):
    config_cals: list[Connections]
    config_upconv: list[Connections]
