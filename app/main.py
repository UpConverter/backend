from fastapi import FastAPI

from . import models, schemas
from .database import SessionLocal, engine


schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/ports", response_model=list[models.Port])
def get_ports():
    ports = [
        models.Port(id=1, value='COM1'),
        models.Port(id=2, value='COM2'),
        models.Port(id=3, value='COM3'),
        models.Port(id=4, value='COM4')
    ]
    return ports


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
