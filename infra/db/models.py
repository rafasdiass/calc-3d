"""
Modelos de domínio: Tenant e User.

Roles RBAC:
    owner   → acesso total ao tenant
    editor  → CRUD de projetos
    viewer  → somente leitura
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.db.base import Base, generate_uuid


class UserRole(str, enum.Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class Tenant(Base):
    """Representa um espaço isolado de um cliente/organização."""

    __tablename__ = "tenants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=generate_uuid,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Feature flags como JSONB — preenchido em S1
    # feature_flags: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)

    users: Mapped[list[User]] = relationship("User", back_populates="tenant", lazy="noload")

    def __repr__(self) -> str:
        return f"<Tenant id={self.id} slug={self.slug}>"


class User(SQLAlchemyBaseUserTableUUID, Base):
    """
    Usuário do sistema.

    Herda campos de FastAPI Users (email, hashed_password, is_active, is_superuser,
    is_verified) e acrescenta tenant + RBAC.
    """

    __tablename__ = "users"

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"),
        default=UserRole.VIEWER,
        nullable=False,
    )
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    tenant: Mapped[Tenant] = relationship("Tenant", back_populates="users", lazy="noload")

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} role={self.role}>"
