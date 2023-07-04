from pydantic import BaseModel


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
