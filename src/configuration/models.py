from pydantic import BaseModel


class ConfigurationBase(BaseModel):
    name: str


class Configuration(ConfigurationBase):
    id: int

    class Config:
        orm_mode = True


class ConfigurationCreate(ConfigurationBase):
    pass
