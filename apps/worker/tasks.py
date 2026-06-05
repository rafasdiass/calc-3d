"""
Celery worker — task definitions.

Sprint 0: Celery app wired to Redis broker, no tasks yet.
Sprint 1+: calculation tasks registered here.
"""

from __future__ import annotations

from celery import Celery

from apps.api.config import settings

celery_app = Celery(
    "calc3d",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    # Autodiscover tasks from registered apps
    include=["apps.worker.tasks"],
)

# ─── Stub tasks (Sprint 1+) ───────────────────────────────────────────────────
# @celery_app.task(bind=True, name="calc3d.calculate_project")
# def calculate_project(self, project_id: str, tenant_id: str) -> dict[str, object]:
#     ...
