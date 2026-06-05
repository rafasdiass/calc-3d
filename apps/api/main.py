"""
calc-3d — FastAPI application entry point.

Sprint 0: /health, /version endpoints.
Sprint 1+: routers mounted under /api/v1/
"""

from __future__ import annotations

import time
from typing import Any

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from apps.api.config import settings

logger = structlog.get_logger(__name__)

# ─── Application factory ──────────────────────────────────────────────────────

def create_app() -> FastAPI:
    app = FastAPI(
        title="calc-3d API",
        description="Structural engineering SaaS — FEM + NBR/EC dimensioning engine",
        version=settings.APP_VERSION,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    _register_middleware(app)
    _register_routes(app)

    return app


def _register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def log_requests(request: Request, call_next: Any) -> Any:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed = time.perf_counter() - start
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(elapsed * 1000, 2),
        )
        return response


def _register_routes(app: FastAPI) -> None:
    # ── Infrastructure endpoints (no versioning) ──────────────────────────────

    @app.get("/health", tags=["infra"], summary="Health check")
    async def health() -> JSONResponse:
        return JSONResponse({"status": "ok"})

    @app.get("/version", tags=["infra"], summary="API version")
    async def version() -> JSONResponse:
        return JSONResponse(
            {
                "version": settings.APP_VERSION,
                "env": settings.APP_ENV,
            }
        )

    # ── Versioned API (v1) ────────────────────────────────────────────────────
    # Routers are imported lazily to avoid circular deps at import time.
    # Sprint 1+: uncomment as routers are implemented.
    #
    # from apps.api.routers import auth, projects
    # app.include_router(auth.router, prefix="/api/v1")
    # app.include_router(projects.router, prefix="/api/v1")


# ─── Module-level app instance (used by uvicorn) ──────────────────────────────
app = create_app()
