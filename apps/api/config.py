"""
Application settings — loaded from environment variables / .env file.
Uses Pydantic v2 BaseSettings for type-safe config.
"""

from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_ENV: str = "development"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_VERSION: str = "0.1.0"
    SECRET_KEY: str = "insecure-dev-secret"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://calc3d:calc3d@localhost:5432/calc3d"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://calc3d:calc3d@localhost:5432/calc3d"

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    # JWT
    JWT_SECRET: str = "insecure-dev-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # Rate limiting
    RATE_LIMIT_FREE: int = 60
    RATE_LIMIT_PRO: int = 600

    # Observability
    SENTRY_DSN: str = ""
    LOG_LEVEL: str = "INFO"

    @field_validator("APP_ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {allowed}")
        return v


settings = Settings()
