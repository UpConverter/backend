from typing import Any

from pydantic import BaseSettings, PostgresDsn, root_validator

from src.constants import Environment


class Config(BaseSettings):
    # SQLite db
    DATABASE_URL = "sqlite:///./test.db"
    # Для PostgreSQL:
    # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/db_name"
    # Или
    # DATABASE_URL: PostgresDsn
    # REDIS_URL: RedisDsn

    # SITE_DOMAIN: str = "myapp.com"

    # ENVIRONMENT: Environment = Environment.PRODUCTION
    ENVIRONMENT: Environment = Environment.LOCAL

    SENTRY_DSN: str | None = "100"

    CORS_ORIGINS: list[str] = ["http://localhost:8000"]
    CORS_ORIGINS_REGEX: str | None
    CORS_HEADERS: list[str] = ["*"]

    APP_VERSION: str = "1"

    @root_validator(skip_on_failure=True)
    def validate_sentry_non_local(cls, data: dict[str, Any]) -> dict[str, Any]:
        if data["ENVIRONMENT"].is_deployed and not data["SENTRY_DSN"]:
            raise ValueError("Sentry is not set")

        return data


settings = Config()

app_configs: dict[str, Any] = {"title": "UpConverter API"}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

if not settings.ENVIRONMENT.is_debug:
    app_configs["openapi_url"] = None  # hide docs
