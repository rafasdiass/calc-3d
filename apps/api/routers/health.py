"""Rotas de saúde e versão — não requerem autenticação."""
from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter

from apps.api.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", summary="Health check")
async def health() -> dict[str, str]:
    """Retorna status 200 se o processo está vivo."""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@router.get("/version", summary="Versão da API")
async def version() -> dict[str, str]:
    """Retorna nome e versão da aplicação."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "env": settings.ENV,
    }
