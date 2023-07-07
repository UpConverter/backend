from typing import Optional

from pydantic import BaseModel


class ConnectionCreate(BaseModel):
    device_id: int
    connected_to_device_id: Optional[int]
    connected_to_device_channel_id: Optional[int]


class Connection(BaseModel):
    id: int
    configuration_id: int
    device_id: int
    connected_to_device_id: Optional[int]
    connected_to_device_channel_id: int


class Connections(BaseModel):
    id: int
    device_id: int
    device_name: str
    model_name: Optional[str]
    state_name: Optional[str]
    connected_to_device_id: Optional[int]
    connected_to_device: Optional[str]
    connected_to_device_channel_id: Optional[int]
    connected_to_device_channel: Optional[str]

    class Config:
        orm_mode = True


class ConnectionsTyped(BaseModel):
    config_cals: list[Connections]
    config_upconv: list[Connections]
