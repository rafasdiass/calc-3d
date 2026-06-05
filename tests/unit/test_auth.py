"""
Testes unitários — auth router (Sprint 0 stubs).

Cobertura:
  - POST /api/auth/register → 201 + UserRead tipado
  - POST /api/auth/token → 200 + Token com access_token
  - POST /api/auth/token sem campos → 422
"""
import pytest
from fastapi.testclient import TestClient

from apps.api.main import create_app

_app = create_app()
_client = TestClient(_app, raise_server_exceptions=True)

_VALID_PAYLOAD = {
    "email": "test@example.com",
    "password": "supersecret123",
    "tenant_id": "acme-corp",
}


class TestRegister:
    def test_register_returns_201(self) -> None:
        response = _client.post("/api/auth/register", json=_VALID_PAYLOAD)
        assert response.status_code == 201

    def test_register_response_contains_email(self) -> None:
        response = _client.post("/api/auth/register", json=_VALID_PAYLOAD)
        body = response.json()
        assert body["email"] == _VALID_PAYLOAD["email"]

    def test_register_response_contains_tenant_id(self) -> None:
        response = _client.post("/api/auth/register", json=_VALID_PAYLOAD)
        body = response.json()
        assert body["tenant_id"] == _VALID_PAYLOAD["tenant_id"]

    def test_register_response_has_id(self) -> None:
        response = _client.post("/api/auth/register", json=_VALID_PAYLOAD)
        body = response.json()
        assert "id" in body
        assert isinstance(body["id"], str)

    def test_register_does_not_expose_password(self) -> None:
        response = _client.post("/api/auth/register", json=_VALID_PAYLOAD)
        body = response.json()
        assert "password" not in body

    def test_register_invalid_email_returns_422(self) -> None:
        payload = {**_VALID_PAYLOAD, "email": "not-an-email"}
        response = _client.post("/api/auth/register", json=payload)
        assert response.status_code == 422

    def test_register_short_password_returns_422(self) -> None:
        payload = {**_VALID_PAYLOAD, "password": "short"}
        response = _client.post("/api/auth/register", json=payload)
        assert response.status_code == 422


class TestToken:
    def test_token_returns_200(self) -> None:
        response = _client.post("/api/auth/token", json=_VALID_PAYLOAD)
        assert response.status_code == 200

    def test_token_response_has_access_token(self) -> None:
        response = _client.post("/api/auth/token", json=_VALID_PAYLOAD)
        body = response.json()
        assert "access_token" in body
        assert isinstance(body["access_token"], str)
        assert len(body["access_token"]) > 0

    def test_token_response_type_is_bearer(self) -> None:
        response = _client.post("/api/auth/token", json=_VALID_PAYLOAD)
        body = response.json()
        assert body["token_type"] == "bearer"
