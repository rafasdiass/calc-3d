"""
Celery application + Sprint 0 placeholder tasks.

Sprint 0: apenas declara o app e uma task dummy para validar wiring.
Sprint 1: tasks reais de cálculo estrutural (calc_foundation, export_report, etc.).

Configuração via env:
  CELERY_BROKER_URL  (default: redis://localhost:6379/0)
  CELERY_RESULT_BACKEND (default: redis://localhost:6379/1)
"""
from __future__ import annotations

import logging
import os

from celery import Celery

logger = logging.getLogger(__name__)

_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "calc3d_worker",
    broker=_BROKER_URL,
    backend=_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    # Sprint 1: adicionar task_routes para separar filas por tipo de cálculo
)


@celery_app.task(name="worker.ping", bind=True)
def ping(self: object) -> dict[str, str]:  # type: ignore[type-arg]
    """Sprint 0 smoke-test task. Retorna pong com task_id."""
    task_id: str = getattr(self, "request", None) and self.request.id or "unknown"  # type: ignore[union-attr]
    logger.info("ping recebido — task_id=%s", task_id)
    return {"status": "pong", "task_id": task_id}


# Sprint 1: adicionar tasks aqui
# @celery_app.task(name="worker.calc_foundation")
# async def calc_foundation(payload: dict) -> dict: ...
