"""
Schemas Pydantic para User: Create, Read, Update.
Expostos no OpenAPI via FastAPI Users.
"""
from __future__ import annotations

import uuid

from fastapi_users import schemas
from pydantic import EmailStr, Field

from infra.db.models import UserRole


class UserRead(schemas.BaseUser[uuid.UUID]):
    """Resposta pública de um usuário."""

    tenant_id: uuid.UUID
    role: UserRole
    full_name: str | None = None


class UserCreate(schemas.BaseUserCreate):
    """Payload de criação de usuário (signup)."""

    tenant_id: uuid.UUID
    role: UserRole = UserRole.VIEWER
    full_name: str | None = Field(default=None, max_length=255)


class UserUpdate(schemas.BaseUserUpdate):
    """Payload de atualização parcial de usuário."""

    full_name: str | None = Field(default=None, max_length=255)
    role: UserRole | None = None
