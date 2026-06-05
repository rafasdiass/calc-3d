"""
Database session factory — Sprint 0 stub.

Sprint 1: substituir pelo engine asyncpg + SQLAlchemy 2.x async.

Configuração via env:
  DATABASE_URL  (ex: postgresql+asyncpg://user:pass@host:5432/calc3d)
"""
from __future__ import annotations

import os
from typing import AsyncGenerator

# Sprint 1: from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL: str = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://calc3d:calc3d@localhost:5432/calc3d",
)

# Sprint 1: descomentarizar
# engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
# async_session_factory = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[None, None]:  # Sprint 1: AsyncGenerator[AsyncSession, None]
    """Dependency para injeção de sessão assíncrona de banco de dados.

    Sprint 0: yield None como placeholder seguro.
    Sprint 1: yield async_session_factory() com context manager.
    """
    # TODO Sprint 1:
    # async with async_session_factory() as session:
    #     yield session
    yield None  # type: ignore[misc]
