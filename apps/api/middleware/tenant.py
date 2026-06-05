"""
Middleware que extrai tenant_id do JWT e o injeta no contexto do request.

Fluxo:
    1. Decodifica o JWT do header Authorization (sem verificar assinatura aqui —
       FastAPI Users já verifica no endpoint protegido).
    2. Extrai o campo tenant_id do payload.
    3. Armazena em request.state.tenant_id para uso nos endpoints.

Nota: O SET LOCAL do PostgreSQL RLS é feito no event listener da sessão
SQLAlchemy (infra/db/session.py), não aqui.
"""
from __future__ import annotations

import uuid

import structlog
from fastapi import Request, Response
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from apps.api.config import get_settings

log = structlog.get_logger()
_settings = get_settings()

# Rotas que não exigem tenant_id no estado
_BYPASS_PATHS: frozenset[str] = frozenset(
    {
        f"{_settings.api_v1_prefix}/health",
        f"{_settings.api_v1_prefix}/version",
        f"{_settings.api_v1_prefix}/auth/jwt/login",
        f"{_settings.api_v1_prefix}/auth/register",
        f"{_settings.api_v1_prefix}/auth/forgot-password",
        f"{_settings.api_v1_prefix}/auth/reset-password",
        "/docs",
        "/redoc",
        "/openapi.json",
        "/metrics",
    }
)


class TenantMiddleware(BaseHTTPMiddleware):
    """Extrai tenant_id do JWT e o disponibiliza em request.state.tenant_id."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        request.state.tenant_id = None

        if request.url.path in _BYPASS_PATHS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header.removeprefix("Bearer ").strip()
            try:
                payload = jwt.decode(
                    token,
                    _settings.secret_key,
                    algorithms=[_settings.jwt_algorithm],
                    options={"verify_exp": True},
                )
                raw_tenant_id: str | None = payload.get("tenant_id")
                if raw_tenant_id:
                    request.state.tenant_id = uuid.UUID(raw_tenant_id)
            except (JWTError, ValueError):
                # Silencioso: o endpoint protegido vai rejeitar se necessário
                log.warning("tenant_middleware.invalid_jwt", path=request.url.path)

        return await call_next(request)
