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
    timestamp: datetime

    class Config:
        orm_mode = True


class AttemptStatus(Attempt):
    attempt_token: str


class AttemptRelatedCreate(BaseModel):
    configuration_id: int
    speed: int
    port: str


class AttemptRelated(AttemptRelatedCreate):
    id: int
    configuration: str


class AttemptConnections(ConnectionsTyped):
    attempt: AttemptRelated
    attempt_token: str
