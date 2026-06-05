"""SQLAlchemy async engine + session factory.

Mecanismo de injeção de tenant_id (ADR-0004):
  - `before_cursor_execute` → SET LOCAL app.tenant_id = :tid (escopo transação)
  - checkin do pool         → RESET app.tenant_id          (cinto-e-suspensório)

O `contextvars.ContextVar` `_tenant_id_ctx` é populado pelo middleware
FastAPI (apps/api/middleware/tenant.py) antes de cada request.
"""
from __future__ import annotations

import contextvars
import uuid
from collections.abc import AsyncGenerator

from sqlalchemy import event, text
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import AsyncAdaptedQueuePool

from apps.api.config import settings

# ── ContextVar: populada pelo TenantMiddleware ────────────────────────────────
_tenant_id_ctx: contextvars.ContextVar[uuid.UUID | None] = contextvars.ContextVar(
    "_tenant_id_ctx", default=None
)


def set_tenant_context(tenant_id: uuid.UUID) -> None:
    """Chamada pelo middleware após validar o JWT."""
    _tenant_id_ctx.set(tenant_id)


def get_tenant_context() -> uuid.UUID | None:
    return _tenant_id_ctx.get()


# ── Engine ────────────────────────────────────────────────────────────────────

def _build_engine() -> AsyncEngine:
    return create_async_engine(
        str(settings.DATABASE_URL),
        echo=settings.DB_ECHO,
        poolclass=AsyncAdaptedQueuePool,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,
    )


engine: AsyncEngine = _build_engine()

# ── Session factory ───────────────────────────────────────────────────────────

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# ── RLS hooks ─────────────────────────────────────────────────────────────────

@event.listens_for(engine.sync_engine, "before_cursor_execute")
def _inject_tenant_id(
    conn: AsyncConnection,  # type: ignore[type-arg]
    cursor: object,
    statement: str,
    parameters: object,
    context: object,
    executemany: bool,
) -> None:
    """SET LOCAL app.tenant_id garante escopo de transação (ADR-0004)."""
    tid = _tenant_id_ctx.get()
    if tid is not None:
        cursor.execute(  # type: ignore[union-attr]
            f"SET LOCAL app.tenant_id = '{tid}'"
        )


# ── Dependency FastAPI ────────────────────────────────────────────────────────

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency que fornece uma sessão async por request."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
