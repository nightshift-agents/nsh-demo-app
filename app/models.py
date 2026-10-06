from datetime import date

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    isbn: str = Field(min_length=10, max_length=17)
    year: int | None = Field(default=None, ge=1450, le=2100)


class Book(BookCreate):
    id: int


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: str = Field(min_length=3, max_length=254)


class Member(MemberCreate):
    id: int
    joined_at: date


class LoanCreate(BaseModel):
    book_id: int
    member_id: int
    due_date: date | None = None


class Loan(BaseModel):
    id: int
    book_id: int
    member_id: int
    loaned_at: date
    due_date: date
    returned_at: date | None = None

    @property
    def is_active(self) -> bool:
        return self.returned_at is None
