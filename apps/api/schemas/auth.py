"""Schemas Pydantic para o domínio de autenticação.

Contratos de entrada/saída — nunca expor modelos ORM diretamente.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Signup ───────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    """Payload de criação de usuário + tenant."""

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    tenant_name: str = Field(
        min_length=1,
        max_length=255,
        description="Nome do escritório / empresa. Cria um tenant novo.",
    )

    @field_validator("password")
    @classmethod
    def password_complexity(cls, v: str) -> str:
        has_upper = any(c.isupper() for c in v)
        has_digit = any(c.isdigit() for c in v)
        if not (has_upper and has_digit):
            raise ValueError(
                "Senha deve conter ao menos 1 letra maiúscula e 1 número."
            )
        return v


# ── Read (response) ───────────────────────────────────────────────────────────

class UserRead(BaseModel):
    """Representação pública do usuário — sem campos sensíveis."""

    model_config = {"from_attributes": True}

    id: uuid.UUID
    email: EmailStr
    full_name: str
    tenant_id: uuid.UUID
    role: str
    is_active: bool
    created_at: datetime


# ── Token ─────────────────────────────────────────────────────────────────────

class TokenResponse(BaseModel):
    """Resposta de login/refresh."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Segundos até expirar o access_token")


class RefreshRequest(BaseModel):
    refresh_token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
