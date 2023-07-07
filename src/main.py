from contextlib import asynccontextmanager
from typing import AsyncGenerator

import sentry_sdk
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.attempt.router import router as attempt_router
from src.config import app_configs, settings
from src.configuration.router import router as config_router
from src.connection.router import router as connection_router
from src.database import database
from src.device.router import router as device_router
from src.port.router import router as port_router
from src.speed.router import router as speed_router


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    # Startup
    await database.connect()

    yield

    # Shutdown
    await database.disconnect()


app = FastAPI(**app_configs, lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

if settings.ENVIRONMENT.is_deployed:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
    )


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(port_router, prefix="/ports", tags=["ports"])
app.include_router(speed_router, prefix="/speeds", tags=["speeds"])
app.include_router(device_router, prefix="/devices", tags=["devices"])
app.include_router(connection_router, prefix="/connections",
                   tags=["connections"])
app.include_router(config_router, prefix="/configs", tags=["configs"])
app.include_router(attempt_router, prefix="/attempts", tags=["attempts"])
