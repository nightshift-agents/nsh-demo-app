import pytest
from fastapi.testclient import TestClient


def test_create_member_normalizes_email(client: TestClient) -> None:
    response = client.post("/members", json={"name": "Luis", "email": "  Luis@Example.COM "})
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "luis@example.com"
    assert "joined_at" in body


def test_create_member_rejects_duplicate_email(client: TestClient, member: dict) -> None:
    response = client.post("/members", json={"name": "Otra", "email": "ANA@example.com"})
    assert response.status_code == 409


def test_get_member_404_when_missing(client: TestClient) -> None:
    assert client.get("/members/42").status_code == 404


def test_list_members(client: TestClient, member: dict) -> None:
    assert client.get("/members").json() == [member]


@pytest.mark.parametrize("email", ["no-es-un-correo", "sin-arroba.com", "@dominio.com"])
def test_create_member_rejects_invalid_email(client: TestClient, email: str) -> None:
    response = client.post("/members", json={"name": "X", "email": email})
    assert response.status_code == 422
