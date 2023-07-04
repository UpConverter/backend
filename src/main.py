from fastapi import FastAPI

from src.device.router import router as device_router
from src.attempt.router import router as attempt_router
from src.connection.router import router as connection_router
from src.database import database
from src.config import app_configs, settings

app = FastAPI(**app_configs)


# import sentry_sdk
# from starlette.middleware.cors import CORSMiddleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.CORS_ORIGINS,
#     allow_origin_regex=settings.CORS_ORIGINS_REGEX,
#     allow_credentials=True,
#     allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
#     allow_headers=settings.CORS_HEADERS,
# )

# if settings.ENVIRONMENT.is_deployed:
#     sentry_sdk.init(
#         dsn=settings.SENTRY_DSN,
#         environment=settings.ENVIRONMENT,
#     )

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(attempt_router, prefix="", tags=["port"])
app.include_router(device_router, prefix="", tags=["device"])
app.include_router(connection_router, prefix="", tags=["config"])
