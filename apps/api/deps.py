"""
FastAPI dependency injectors.

Sprint 0: stubs only.
Sprint 1+: db session, current_user, tenant_id are fully wired.
"""

from __future__ import annotations

from typing import AsyncGenerator

# ─── DB session (stub — wired in Sprint 1 after Alembic models exist) ─────────
# from sqlalchemy.ext.asyncio import AsyncSession
# from apps.api.db import async_session_factory
#
# async def get_db() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_factory() as session:
#         yield session


# ─── Auth + tenant (stub — wired in Sprint 1 after FastAPI Users setup) ───────
# async def get_current_user(...) -> User: ...
# async def get_tenant_id(user: User = Depends(get_current_user)) -> UUID: ...


__all__: list[str] = []
