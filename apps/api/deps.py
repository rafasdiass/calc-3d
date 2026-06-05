"""
FastAPI dependency injection — auth, db session, tenant.

Sprint 0: stubs prontos para wiring real na Sprint 1.
"""
from __future__ import annotations

from typing import Annotated, Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------

_bearer_scheme = HTTPBearer(auto_error=False)


def get_current_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(_bearer_scheme),
    ],
) -> str:
    """Extrai o raw JWT do header Authorization: Bearer <token>.

    Levanta 401 se ausente.
    """
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


# ---------------------------------------------------------------------------
# Tenant
# ---------------------------------------------------------------------------


def get_tenant_id(request: Request) -> str:
    """Retorna tenant_id injetado pelo TenantMiddleware.

    Levanta 400 se o middleware não populou — não deve ocorrer em produção.
    """
    tenant_id: str | None = getattr(request.state, "tenant_id", None)
    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tenant não identificado na requisição.",
        )
    return tenant_id


# ---------------------------------------------------------------------------
# DB session (stub — Sprint 1 conecta SQLAlchemy/asyncpg)
# ---------------------------------------------------------------------------


def get_db() -> Generator[None, None, None]:
    """Placeholder para a sessão async de banco de dados.

    Sprint 1: substituir por AsyncSession do SQLAlchemy.
    """
    # TODO: yield AsyncSession(engine)
    yield None  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Type aliases convenientes para injeção nos routers
# ---------------------------------------------------------------------------

CurrentToken = Annotated[str, Depends(get_current_token)]
TenantId = Annotated[str, Depends(get_tenant_id)]
DbSession = Annotated[None, Depends(get_db)]  # Sprint 1: trocar None por AsyncSession
