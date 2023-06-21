from fastapi import FastAPI

from . import router, schemas
from .database import engine


schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(router.router, prefix="", tags=["port"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)
