from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient


def _loan(client: TestClient, book_id: int, member_id: int, **extra) -> dict:
    response = client.post("/loans", json={"book_id": book_id, "member_id": member_id, **extra})
    assert response.status_code == 201, response.text
    return response.json()


def test_create_loan_defaults_due_date_to_14_days(
    client: TestClient, book: dict, member: dict
) -> None:
    loan = _loan(client, book["id"], member["id"])
    assert loan["returned_at"] is None
    assert date.fromisoformat(loan["due_date"]) == date.today() + timedelta(days=14)


def test_create_loan_404_when_book_missing(client: TestClient, member: dict) -> None:
    response = client.post("/loans", json={"book_id": 99, "member_id": member["id"]})
    assert response.status_code == 404


def test_create_loan_404_when_member_missing(client: TestClient, book: dict) -> None:
    response = client.post("/loans", json={"book_id": book["id"], "member_id": 99})
    assert response.status_code == 404


def test_member_cannot_exceed_three_active_loans(client: TestClient, member: dict) -> None:
    for i in range(4):
        client.post("/books", json={"title": f"L{i}", "author": "A", "isbn": f"978000000000{i}"})
    for book_id in (1, 2, 3):
        _loan(client, book_id, member["id"])
    response = client.post("/loans", json={"book_id": 4, "member_id": member["id"]})
    assert response.status_code == 409


def test_return_loan_sets_returned_at(client: TestClient, book: dict, member: dict) -> None:
    loan = _loan(client, book["id"], member["id"])
    response = client.post(f"/loans/{loan['id']}/return")
    assert response.status_code == 200
    assert response.json()["returned_at"] == date.today().isoformat()


def test_return_loan_twice_is_conflict(client: TestClient, book: dict, member: dict) -> None:
    loan = _loan(client, book["id"], member["id"])
    client.post(f"/loans/{loan['id']}/return")
    assert client.post(f"/loans/{loan['id']}/return").status_code == 409


def test_list_loans_filters_by_active(client: TestClient, member: dict) -> None:
    client.post("/books", json={"title": "A", "author": "A", "isbn": "9780000000011"})
    client.post("/books", json={"title": "B", "author": "B", "isbn": "9780000000012"})
    first = _loan(client, 1, member["id"])
    _loan(client, 2, member["id"])
    client.post(f"/loans/{first['id']}/return")
    active = client.get("/loans", params={"active": "true"}).json()
    assert [loan["book_id"] for loan in active] == [2]
    assert len(client.get("/loans", params={"member_id": member["id"]}).json()) == 2


def test_get_loan_404_when_missing(client: TestClient) -> None:
    assert client.get("/loans/7").status_code == 404


@pytest.mark.xfail(reason="Bug conocido: se puede prestar un libro ya prestado", strict=True)
def test_cannot_loan_book_already_on_loan(client: TestClient, book: dict, member: dict) -> None:
    other = client.post("/members", json={"name": "Beto", "email": "beto@example.com"}).json()
    _loan(client, book["id"], member["id"])
    response = client.post("/loans", json={"book_id": book["id"], "member_id": other["id"]})
    assert response.status_code == 409


def test_list_overdue_loans(client: TestClient, book: dict, member: dict) -> None:
    client.post("/books", json={"title": "B", "author": "B", "isbn": "9780000000012"})
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    overdue = _loan(client, book["id"], member["id"], due_date=yesterday)
    _loan(client, 2, member["id"])
    response = client.get("/loans/overdue")
    assert response.status_code == 200
    assert [loan["id"] for loan in response.json()] == [overdue["id"]]
