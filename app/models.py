from pydantic import BaseModel


class Port(BaseModel):
    id: int
    value: str

class Speed(BaseModel):
    id: int
    value: int

class Config(BaseModel):
    id: int
    value: str

class Cal(BaseModel):
    id: int
    value: str

class Channel(BaseModel):
    id: int
    value: str

class Type(BaseModel):
    id: int
    value: str