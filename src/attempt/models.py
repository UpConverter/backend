from pydantic import BaseModel
from datetime import datetime
from src.connection.models import ConnectionsTyped


class AttemptBase(BaseModel):
    configuration_id: int
    speed_id: int
    port_id: int
    success: bool


class AttemptCreate(AttemptBase):
    pass


class Attempt(AttemptBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class AttemptName(AttemptBase):
    config_name: str


class AttemptFull(ConnectionsTyped):
    attempt: AttemptName
