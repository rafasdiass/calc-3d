"""Celery application — Sprint 0 skeleton.

Tarefas reais serão adicionadas a partir da Sprint 1.
"""
from __future__ import annotations

from celery import Celery

from apps.api.config import settings


def create_celery() -> Celery:
    app = Celery(
        "calc3d",
        broker=settings.REDIS_URL,
        backend=settings.REDIS_URL,
        include=[],  # registrar módulos de tasks aqui
    )
    app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_acks_late=True,
        worker_prefetch_multiplier=1,  # fair dispatch para tasks longas
    )
    return app


celery_app: Celery = create_celery()
