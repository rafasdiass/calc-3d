"""
Configuração central da aplicação via Pydantic Settings.
Lida de variáveis de ambiente ou arquivo .env.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────────
    app_name: str = "calc-3d API"
    app_version: str = "0.1.0"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # ── API ──────────────────────────────────────────────────────────────────
    api_v1_prefix: str = "/api/v1"
    allowed_origins: list[str] = Field(
        default=["http://localhost:5173", "http://localhost:3000"],
    )

    # ── Database ─────────────────────────────────────────────────────────────
    database_url: PostgresDsn = Field(
        default="postgresql+asyncpg://calc3d:calc3d@localhost:5432/calc3d",
    )

    # Pool
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_timeout: int = 30

    # ── Redis ────────────────────────────────────────────────────────────────
    redis_url: RedisDsn = Field(default="redis://localhost:6379/0")

    # ── Auth / JWT ───────────────────────────────────────────────────────────
    secret_key: str = Field(
        default="CHANGE-ME-IN-PRODUCTION-use-openssl-rand-hex-32",
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    # ── Sentry ───────────────────────────────────────────────────────────────
    sentry_dsn: str | None = None

    # ── Rate limits ──────────────────────────────────────────────────────────
    rate_limit_free_per_minute: int = 60
    rate_limit_pro_per_minute: int = 600

    # ── Celery ───────────────────────────────────────────────────────────────
    celery_broker_url: str = "redis://localhost:6379/1"
    celery_result_backend: str = "redis://localhost:6379/2"

    # ── Prometheus ───────────────────────────────────────────────────────────
    prometheus_enabled: bool = True

    @field_validator("secret_key")
    @classmethod
    def secret_key_must_not_be_default_in_prod(cls, v: str, info: object) -> str:  # noqa: ANN001
        # Acessamos o dict parcial via info.data se disponível
        data = getattr(info, "data", {})
        if data.get("environment") == "production" and "CHANGE-ME" in v:
            msg = "secret_key não pode ser o padrão em produção."
            raise ValueError(msg)
        return v


@lru_cache
def get_settings() -> Settings:
    """Singleton cacheado para evitar leituras repetidas de .env."""
    return Settings()
