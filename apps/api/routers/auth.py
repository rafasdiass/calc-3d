"""
Auth router — Sprint 0 stub.

POST /api/auth/register  → 201 UserRead
POST /api/auth/token     → 200 Token

Sprint 0: retorna dados mock tipados.
Sprint 1: conectar a infra/db + Argon2 + JWT signing real.
"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from apps.api.schemas.auth import Token, UserCreate, UserRead

router = APIRouter()


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar novo usuário",
)
async def register(payload: UserCreate) -> UserRead:
    """Sprint 0: retorna echo tipado. Sprint 1: persiste no banco."""
    # TODO Sprint 1: verificar email único, hash senha, INSERT users
    return UserRead(
        id="00000000-0000-0000-0000-000000000000",
        email=payload.email,
        tenant_id=payload.tenant_id,
        is_active=True,
    )


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Obter JWT de acesso",
)
async def login(payload: UserCreate) -> Token:
    """Sprint 0: retorna token placeholder. Sprint 1: validar credenciais + assinar JWT."""
    # TODO Sprint 1: buscar usuário, verificar senha, emitir JWT com sub + tenant_id
    if not payload.email or not payload.password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email e senha são obrigatórios.",
        )
    return Token(
        access_token="sprint0.placeholder.token",
        token_type="bearer",
    )
