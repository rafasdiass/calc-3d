"""
Testes de integração para GET /health.

Usa TestClient síncrono (httpx) — não requer banco de dados ativo.
FastAPI TestClient funciona sem EVENT_LOOP real em pytest síncrono.
"""
import pytest
from fastapi.testclient import TestClient

from lct_calculator.apps.api.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


class TestHealthEndpoint:
    def test_health_returns_200(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_ok(self, client: TestClient) -> None:
        body = response = client.get("/health").json()
        assert body["status"] == "ok"

    def test_health_version_present(self, client: TestClient) -> None:
        body = client.get("/health").json()
        assert "version" in body
        assert body["version"] == "0.2.0"

    def test_health_content_type_json(self, client: TestClient) -> None:
        response = client.get("/health")
        assert "application/json" in response.headers["content-type"]
