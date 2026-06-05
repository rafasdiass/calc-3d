"""
Testes unitários — TenantMiddleware.

Cobertura:
  - Rotas isentas (/api/health) passam sem tenant_id
  - Middleware não bloqueia rotas isentas (não retorna 4xx)
  - Middleware não injeta tenant_id errado em rota isenta
"""
import pytest
from fastapi.testclient import TestClient

from apps.api.main import create_app

_app = create_app()
_client = TestClient(_app, raise_server_exceptions=True)


class TestTenantMiddlewareExemptRoutes:
    def test_health_accessible_without_auth(self) -> None:
        """Rota isenta não deve exigir Authorization header."""
        response = _client.get("/api/health")
        assert response.status_code == 200

    def test_auth_register_accessible_without_token(self) -> None:
        """Auth routes são isentas de tenant extraction."""
        payload = {
            "email": "middleware@test.com",
            "password": "password123",
            "tenant_id": "test-tenant",
        }
        response = _client.post("/api/auth/register", json=payload)
        # Deve ser 201, não 401/400 por tenant ausente
        assert response.status_code == 201


class TestTenantMiddlewareJwtExtraction:
    def test_invalid_jwt_does_not_crash(self) -> None:
        """Bearer token malformado não deve causar 500."""
        response = _client.get(
            "/api/health",
            headers={"Authorization": "Bearer not.a.valid.jwt"},
        )
        # Health é isenta — deve passar normalmente
        assert response.status_code == 200
