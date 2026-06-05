"""
Router de saúde e versão da API.

Endpoints:
    GET /api/v1/health   → 200 { status: "ok" }
    GET /api/v1/version  → 200 { version: "0.1.0", ... }
"""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

from apps.api.config import get_settings

router = APIRouter(tags=["health"])

_settings = get_settings()


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    environment: str


class VersionResponse(BaseModel):
    app: str
    version: str
    api_prefix: str
    environment: str


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Retorna 200 quando a aplicação está disponível.",
)
async def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        timestamp=datetime.now(tz=timezone.utc),
        environment=_settings.environment,
    )


@router.get(
    "/version",
    response_model=VersionResponse,
    summary="Versão da API",
)
async def version() -> VersionResponse:
    return VersionResponse(
        app=_settings.app_name,
        version=_settings.app_version,
        api_prefix=_settings.api_v1_prefix,
        environment=_settings.environment,
    )
