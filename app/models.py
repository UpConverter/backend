from pydantic import BaseModel


class PortBase(BaseModel):
    id: int
    name: str


class PortCreate(PortBase):
    pass


class Port(PortBase):
    class Config:
        orm_mode = True


class DeviceTypeBase(BaseModel):
    id: int
    name: str


class DeviceTypeCreate(DeviceTypeBase):
    pass


class DeviceType(DeviceTypeBase):
    pass


class DeviceModelBase(BaseModel):
    id: int
    name: str


class DeviceModelCreate(DeviceModelBase):
    pass


class DeviceModel(DeviceModelBase):
    pass


class DeviceStateBase(BaseModel):
    id: int
    name: str


class DeviceStateCreate(DeviceStateBase):
    pass


class DeviceState(DeviceStateBase):
    pass


class DeviceAdditionalStateBase(BaseModel):
    id: int
    name: str


class DeviceAdditionalStateCreate(DeviceAdditionalStateBase):
    pass


class DeviceAdditionalState(DeviceAdditionalStateBase):
    pass


class ChannelBase(BaseModel):
    id: int
    name: str


class ChannelCreate(ChannelBase):
    pass


class Channel(ChannelBase):
    pass


class SpeedBase(BaseModel):
    id: int
    value: int


class SpeedCreate(SpeedBase):
    pass


class Speed(SpeedBase):
    pass


class DeviceBase(BaseModel):
    id: int
    serial_number: int
    type_id: int
    model_id: int
    state_id: int
    additional_state_id: int


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    pass


class ConnectionBase(BaseModel):
    id: int
    configuration_id: int
    device_id: int
    connected_to_device_id: int
    connected_to_device_channel_id: int


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    pass


class ConfigurationBase(BaseModel):
    id: int
    speed_id: int
    port_id: int
    name: str


class ConfigurationCreate(ConfigurationBase):
    pass


class Configuration(ConfigurationBase):
    pass
