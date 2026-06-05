"""
calc-3d API — FastAPI application factory.

Sprint 0: health + auth endpoints.
Sprint 1+: calculation, projects, results.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.api.middleware.tenant import TenantMiddleware
from apps.api.routers import health, auth


def create_app() -> FastAPI:
    app = FastAPI(
        title="calc-3d API",
        description="Structural foundation calculator — multi-tenant SaaS",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    # --- CORS ---
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # TODO Sprint 1: restringir a origins configuradas
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Tenant extraction (JWT → request.state.tenant_id) ---
    app.add_middleware(TenantMiddleware)

    # --- Routers ---
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

    return app


app = create_app()
