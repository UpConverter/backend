from fastapi import FastAPI

from .routers import port, device, configuration
from . import schemas
from .database import engine


schemas.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(port.router, prefix="", tags=["port"])
app.include_router(device.router, prefix="", tags=["device"])
app.include_router(configuration.router, prefix="", tags=["configuration"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)
