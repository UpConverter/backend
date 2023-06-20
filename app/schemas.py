from sqlalchemy import Column, Integer, String

from .database import Base


class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=True)
