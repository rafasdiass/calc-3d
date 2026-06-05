"""
Health-check router.

GET /api/health  → 200 { status: "ok", version: "0.1.0" }

Sem autenticação — usado por load balancer / uptime monitors.
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    version: str


@router.get("/health", response_model=HealthResponse, status_code=200)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", version="0.1.0")
