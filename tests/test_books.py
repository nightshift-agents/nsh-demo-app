from fastapi.testclient import TestClient


def test_create_book_returns_201_with_id(client: TestClient) -> None:
    payload = {"title": "Rayuela", "author": "Cortázar", "isbn": "9788437604572", "year": 1963}
    response = client.post("/books", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == "Rayuela"
    assert body["year"] == 1963


def test_create_book_rejects_duplicate_isbn(client: TestClient, book: dict) -> None:
    response = client.post("/books", json={k: v for k, v in book.items() if k != "id"})
    assert response.status_code == 409


def test_create_book_rejects_invalid_payload(client: TestClient) -> None:
    response = client.post("/books", json={"title": "", "author": "X", "isbn": "123"})
    assert response.status_code == 422


def test_list_books_filters_by_author(client: TestClient, book: dict) -> None:
    client.post("/books", json={"title": "Ficciones", "author": "Borges", "isbn": "9780802130303"})
    assert len(client.get("/books").json()) == 2
    filtered = client.get("/books", params={"author": "borges"}).json()
    assert [b["title"] for b in filtered] == ["Ficciones"]


def test_get_book_404_when_missing(client: TestClient) -> None:
    response = client.get("/books/999")
    assert response.status_code == 404


def test_delete_book_removes_it(client: TestClient, book: dict) -> None:
    assert client.delete(f"/books/{book['id']}").status_code == 204
    assert client.get(f"/books/{book['id']}").status_code == 404
    assert client.delete(f"/books/{book['id']}").status_code == 404
