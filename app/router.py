from fastapi import APIRouter, HTTPException, Path, Depends
from .database import SessionLocal
from sqlalchemy.orm import Session
from .models import Port

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ports", response_model=list[Port])
def get_ports():
    ports = [
        Port(id=1, value='COM1'),
        Port(id=2, value='COM2'),
    ]
    return ports