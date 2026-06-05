"""
Engine assíncrona e fábrica de sessões SQLAlchemy.
"""
from __future__ import annotations

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from apps.api.config import get_settings

_settings = get_settings()

engine = create_async_engine(
    str(_settings.database_url),
    pool_size=_settings.db_pool_size,
    max_overflow=_settings.db_max_overflow,
    pool_timeout=_settings.db_pool_timeout,
    pool_pre_ping=True,
    # Garante reset entre requests (isolation multi-tenant via SET LOCAL)
    pool_reset_on_return="rollback",
    echo=_settings.debug,
)

AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency FastAPI: injeta sessão assíncrona por request.
    Faz rollback automático em caso de exceção.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
