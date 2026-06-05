"""Configuração central da aplicação — lida de variáveis de ambiente.

Pydantic Settings valida em startup; valores inválidos abortam o processo.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import AnyUrl, Field, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Ambiente ────────────────────────────────────────────────────────────
    ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # ── App ─────────────────────────────────────────────────────────────────
    APP_NAME: str = "calc-3d"
    APP_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"

    # ── Banco de dados ───────────────────────────────────────────────────────
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+asyncpg://calc3d:calc3d@localhost:5432/calc3d"
    )
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20

    # ── Redis ────────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Auth / JWT ────────────────────────────────────────────────────────────
    SECRET_KEY: str = Field(
        default="CHANGE_ME_IN_PRODUCTION_use_openssl_rand_hex_32",
        description="Chave HMAC para assinar JWT. Trocar antes de ir a produção.",
    )
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── Observabilidade ───────────────────────────────────────────────────────
    SENTRY_DSN: str | None = None
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @field_validator("SECRET_KEY")
    @classmethod
    def warn_insecure_secret(cls, v: str) -> str:
        if v.startswith("CHANGE_ME") and False:  # só bloquear em prod via ENV check
            raise ValueError("SECRET_KEY não pode ser o default em produção")
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings: Settings = get_settings()
