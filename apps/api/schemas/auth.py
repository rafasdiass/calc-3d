"""
Auth schemas — Pydantic v2.

UserCreate  → input de registro/login
UserRead    → response de usuário (sem senha)
Token       → response de autenticação JWT
"""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Payload de criação de conta / login."""

    email: EmailStr = Field(..., description="Email do usuário")
    password: str = Field(..., min_length=8, description="Senha (mínimo 8 caracteres)")
    tenant_id: str = Field(..., description="Identificador do tenant (slug ou UUID)")


class UserRead(BaseModel):
    """Representação pública do usuário — nunca expõe hash de senha."""

    id: str = Field(..., description="UUID do usuário")
    email: EmailStr
    tenant_id: str
    is_active: bool


class Token(BaseModel):
    """Resposta de autenticação bem-sucedida."""

    access_token: str
    token_type: str = "bearer"
