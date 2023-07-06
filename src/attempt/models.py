from datetime import datetime

from pydantic import BaseModel

from src.connection.models import ConnectionsTyped


class AttemptBase(BaseModel):
    configuration_id: int
    speed_id: int
    port_id: int


class AttemptCreate(AttemptBase):
    pass


class Attempt(AttemptBase):
    id: int
    success: bool
    timestamp: datetime

    class Config:
        orm_mode = True


class AttemptName(AttemptBase):
    config_name: str


class AttemptFull(ConnectionsTyped):
    attempt: AttemptName
