from datetime import datetime

from pydantic import BaseModel


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


class AttemptRelatedCreate(BaseModel):
    configuration_id: int
    speed: int
    port: str


class AttemptRelated(AttemptRelatedCreate):
    configuration: str
    success: bool
