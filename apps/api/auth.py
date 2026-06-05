"""
Configuração de FastAPI Users: backend JWT, manager e router.
"""
from __future__ import annotations

import uuid
from typing import Any

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.config import get_settings
from infra.db.models import User
from infra.db.session import get_async_session

_settings = get_settings()


# ── DB adapter ────────────────────────────────────────────────────────────────


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> SQLAlchemyUserDatabase[User, uuid.UUID]:  # type: ignore[type-arg]
    yield SQLAlchemyUserDatabase(session, User)  # type: ignore[misc]


# ── User Manager ──────────────────────────────────────────────────────────────


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = _settings.secret_key
    verification_token_secret = _settings.secret_key

    async def on_after_register(
        self,
        user: User,
        request: Request | None = None,
    ) -> None:
        import structlog

        log = structlog.get_logger()
        log.info("user_registered", user_id=str(user.id), email=user.email)

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ) -> None:
        import structlog

        log = structlog.get_logger()
        log.info("password_reset_requested", user_id=str(user.id))

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Request | None = None,
    ) -> None:
        import structlog

        log = structlog.get_logger()
        log.info("verification_requested", user_id=str(user.id))


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase[User, uuid.UUID] = Depends(get_user_db),  # type: ignore[type-arg]
) -> UserManager:
    yield UserManager(user_db)


# ── JWT Strategy ──────────────────────────────────────────────────────────────


def get_jwt_strategy() -> JWTStrategy[User, uuid.UUID]:  # type: ignore[type-arg]
    return JWTStrategy(
        secret=_settings.secret_key,
        lifetime_seconds=_settings.access_token_expire_minutes * 60,
        algorithm=_settings.jwt_algorithm,
    )


bearer_transport = BearerTransport(tokenUrl="/api/v1/auth/jwt/login")

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# ── FastAPIUsers instance ─────────────────────────────────────────────────────

fastapi_users = FastAPIUsers[User, uuid.UUID](  # type: ignore[type-arg]
    get_user_manager,
    [auth_backend],
)

# ── Exported dependencies ─────────────────────────────────────────────────────

current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
