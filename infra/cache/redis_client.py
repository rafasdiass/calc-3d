"""
Redis cache client — Sprint 0 stub.

Sprint 1: conectar via redis.asyncio com pool configurado.

Configuração via env:
  REDIS_URL  (ex: redis://localhost:6379/0)
"""
from __future__ import annotations

import os

REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Sprint 1:
# import redis.asyncio as aioredis
# redis_client = aioredis.from_url(REDIS_URL, decode_responses=True)


async def get_cache() -> None:
    """Placeholder de injeção do cliente Redis.

    Sprint 1: retornar redis_client tipado.
    """
    # TODO Sprint 1: return redis_client
    return None
