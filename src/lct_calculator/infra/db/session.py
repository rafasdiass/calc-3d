"""
SQLAlchemy async engine + session factory.

Configuração via variável de ambiente DATABASE_URL (obrigatória em produção).
Fallback para SQLite em memória apenas em ambiente de teste unitário.
"""
import os
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

_DATABASE_URL: str = os.environ.get(
    "DATABASE_URL",
    "sqlite+aiosqlite:///:memory:",  # fallback seguro apenas para testes
)

engine = create_async_engine(
    _DATABASE_URL,
    echo=False,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base declarativa compartilhada por todos os modelos ORM."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency FastAPI que fornece uma sessão de banco de dados.

    Usage:
        @router.get("/")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session
