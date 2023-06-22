from fastapi import APIRouter, HTTPException, Path, Depends
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..models import Port
from ..crud import read_ports

router = APIRouter()


@router.get("/ports", response_model=list[Port])
def get_ports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    ports = read_ports(db, skip=skip, limit=limit)
    return ports
