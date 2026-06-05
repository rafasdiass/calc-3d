"""
TenantMiddleware — extrai tenant_id do JWT e injeta em request.state.

Sprint 0: decodificação sem verificação de assinatura (HS256 placeholder).
Sprint 1: verificar assinatura com chave configurada via env SECRET_KEY.

Rotas isentas (passthrough sem tenant):
  - /api/health
  - /api/auth/*
  - /api/docs, /api/redoc, /api/openapi.json
"""
from __future__ import annotations

import base64
import json
import logging
from typing import Final

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

_EXEMPT_PREFIXES: Final[tuple[str, ...]] = (
    "/api/health",
    "/api/auth/",
    "/api/docs",
    "/api/redoc",
    "/api/openapi.json",
)


def _decode_jwt_payload_unverified(token: str) -> dict[str, object]:
    """Decodifica o payload do JWT sem verificar assinatura.

    Sprint 0: suficiente para extrair tenant_id em ambiente dev.
    Sprint 1: substituir por jose.jwt.decode() com verificação de chave.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:  # noqa: PLR2004
            return {}
        # Adicionar padding base64url
        payload_b64 = parts[1] + "=" * (-len(parts[1]) % 4)
        payload_bytes = base64.urlsafe_b64decode(payload_b64)
        return json.loads(payload_bytes)  # type: ignore[no-any-return]
    except Exception:  # noqa: BLE001
        return {}


class TenantMiddleware(BaseHTTPMiddleware):
    """Popula request.state.tenant_id a partir do claim 'tenant_id' do JWT."""

    async def dispatch(self, request: Request, call_next: object) -> Response:
        # Bypass para rotas isentas
        path = request.url.path
        if any(path.startswith(prefix) for prefix in _EXEMPT_PREFIXES):
            return await call_next(request)  # type: ignore[operator]

        tenant_id: str | None = None

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.removeprefix("Bearer ").strip()
            payload = _decode_jwt_payload_unverified(token)
            tenant_id = payload.get("tenant_id") or payload.get("sub")  # type: ignore[assignment]

        request.state.tenant_id = tenant_id

        if tenant_id is None:
            logger.debug("Requisição sem tenant_id resolvido: %s %s", request.method, path)

        return await call_next(request)  # type: ignore[operator]
