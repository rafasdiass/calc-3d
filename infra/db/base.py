"""Base declarativa + mixins compartilhados.

Toda tabela de domínio herda de `Base`. Tabelas com escopo de tenant
também herdam de `TenantMixin` — o campo `tenant_id` ativa o RLS.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base declarativa única para todo o ORM."""
    pass


class TimestampMixin:
    """Campos `created_at` / `updated_at` gerenciados pelo banco."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class TenantMixin:
    """Coluna `tenant_id` em toda tabela com escopo de tenant.

    A coluna é indexada mas a política de isolamento real está no
    Postgres RLS (ADR-0004). Não dependa apenas do filtro ORM.
    """

    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )
