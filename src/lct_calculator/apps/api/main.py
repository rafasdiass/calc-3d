from fastapi import FastAPI

from lct_calculator.apps.api.routers.health import router as health_router

app = FastAPI(
    title="LCT Calculator API",
    description="API para cálculos de fundações estruturais — Sprint 0 (Fase 0: Fundação Técnica)",
    version="0.2.0",
)

app.include_router(health_router)
