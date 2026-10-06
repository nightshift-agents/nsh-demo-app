from fastapi import APIRouter, HTTPException, status

from app.models import Book, BookCreate
from app.storage import StoreDep

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, store: StoreDep) -> Book:
    if any(b.isbn == payload.isbn for b in store.books.values()):
        raise HTTPException(status.HTTP_409_CONFLICT, f"ISBN {payload.isbn} ya registrado")
    book = Book(id=store.next_id("books"), **payload.model_dump())
    store.books[book.id] = book
    return book


@router.get("", response_model=list[Book])
def list_books(store: StoreDep, author: str | None = None) -> list[Book]:
    books = list(store.books.values())
    if author:
        needle = author.casefold()
        books = [b for b in books if needle in b.author.casefold()]
    return books


@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, store: StoreDep) -> Book:
    book = store.books.get(book_id)
    if book is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Libro {book_id} no existe")
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, store: StoreDep) -> None:
    if book_id not in store.books:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Libro {book_id} no existe")
    del store.books[book_id]
