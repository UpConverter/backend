from sqlalchemy.orm import Session
from . import models, schemas

def read_ports(db: Session, skip: int = 0, limit: int = 100):
    return db.query(schemas.Port).offset(skip).limit(limit).all()
