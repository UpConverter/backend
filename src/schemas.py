from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class DeviceType(Base):
    __tablename__ = "device_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class DeviceModel(Base):
    __tablename__ = "device_model"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class DeviceState(Base):
    __tablename__ = "device_state"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class DeviceAdditionalState(Base):
    __tablename__ = "device_additional_state"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class Channel(Base):
    __tablename__ = "channel"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class Speed(Base):
    __tablename__ = "speed"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, unique=True)


class Port(Base):
    __tablename__ = "port"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)


class Device(Base):
    __tablename__ = "device"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    serial_number = Column(Integer, unique=True)
    type_id = Column(Integer, ForeignKey("device_type.id"))
    model_id = Column(Integer, ForeignKey("device_model.id"))
    state_id = Column(Integer, ForeignKey("device_state.id"))
    additional_state_id = Column(
        Integer, ForeignKey("device_additional_state.id"))

    type_ = relationship("DeviceType", backref="devices")
    model = relationship("DeviceModel", backref="devices")
    state = relationship("DeviceState", backref="devices")
    additional_state = relationship("DeviceAdditionalState", backref="devices")


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    device_id = Column(Integer, ForeignKey("device.id"))
    connected_to_device_id = Column(Integer, ForeignKey("device.id"))
    connected_to_device_channel_id = Column(Integer, ForeignKey("channel.id"))

    configuration = relationship("Configuration", backref="connections")
    device = relationship("Device", foreign_keys=[
                          device_id], backref="connections_as_device")
    connected_to_device = relationship("Device", foreign_keys=[
                                       connected_to_device_id], backref="connections_as_connected_to_device")
    connected_to_device_channel = relationship(
        "Channel", backref="connections")


class Configuration(Base):
    __tablename__ = "configuration"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Attempt(Base):
    __tablename__ = "attempt"

    id = Column(Integer, primary_key=True, index=True)
    configuration_id = Column(Integer, ForeignKey("configuration.id"))
    speed_id = Column(Integer, ForeignKey("speed.id"))
    port_id = Column(Integer, ForeignKey("port.id"))
    success = Column(Boolean)
    timestamp = Column(DateTime)

    configuration = relationship("Configuration", backref="attempts")
    speed = relationship("Speed", backref="attempts")
    port = relationship("Port", backref="attempts")
