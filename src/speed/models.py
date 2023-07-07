from pydantic import BaseModel


class Speed(BaseModel):
    id: int
    value: int

    class Config:
        orm_mode = True
