"""
Testes unitários — health router.

Cobertura:
  - GET /api/health → 200 + body tipado
"""
import pytest
from fastapi.testclient import TestClient

from apps.api.main import create_app

_app = create_app()
_client = TestClient(_app, raise_server_exceptions=True)


class TestHealthEndpoint:
    def test_returns_200(self) -> None:
        response = _client.get("/api/health")
        assert response.status_code == 200

    def test_body_has_status_ok(self) -> None:
        response = _client.get("/api/health")
        body = response.json()
        assert body["status"] == "ok"

    def test_body_has_version(self) -> None:
        response = _client.get("/api/health")
        body = response.json()
        assert "version" in body
        assert isinstance(body["version"], str)
        assert len(body["version"]) > 0
