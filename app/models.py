from pydantic import BaseModel

# class ItemBase(BaseModel):
#     title: str
#     description: str | None = None

# class ItemCreate(ItemBase):
#     pass

# class Item(ItemBase):
#     id: int
#     owner_id: int

#     class Config:
#         orm_mode = True


class PortBase(BaseModel):
    id: int
    value: str


class PortCreate(PortBase):
    pass


class Port(PortBase):
    pass

# class Port(BaseModel):
#     id: int
#     value: str

# class Speed(BaseModel):
#     id: int
#     value: int

# class Config(BaseModel):
#     id: int
#     value: str

# class Cal(BaseModel):
#     id: int
#     value: str

# class Channel(BaseModel):
#     id: int
#     value: str

# class Type(BaseModel):
#     id: int
#     value: str
