from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import store


@pytest.fixture(autouse=True)
def clean_store() -> Iterator[None]:
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def book(client: TestClient) -> dict:
    payload = {"title": "Cien años de soledad", "author": "García Márquez", "isbn": "9780307474728"}
    return client.post("/books", json=payload).json()


@pytest.fixture
def member(client: TestClient) -> dict:
    payload = {"name": "Ana Torres", "email": "ana@example.com"}
    return client.post("/members", json=payload).json()
