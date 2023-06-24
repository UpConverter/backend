from fastapi import APIRouter, HTTPException, Path, Depends
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from ..models import Configuration
from ..crud import read_configurations

router = APIRouter()


@router.get("/configurations", response_model=list[Configuration])
def get_configurations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    configurations = read_configurations(db, skip=skip, limit=limit)
    return configurations
