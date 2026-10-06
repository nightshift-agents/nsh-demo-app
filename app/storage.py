from dataclasses import dataclass, field
from itertools import count
from typing import Annotated

from fastapi import Depends

from app.models import Book, Loan, Member


@dataclass
class Store:
    """Almacenamiento en memoria. Se pierde al reiniciar el proceso."""

    books: dict[int, Book] = field(default_factory=dict)
    members: dict[int, Member] = field(default_factory=dict)
    loans: dict[int, Loan] = field(default_factory=dict)
    _counters: dict[str, count] = field(default_factory=dict)

    def next_id(self, table: str) -> int:
        if table not in self._counters:
            self._counters[table] = count(1)
        return next(self._counters[table])

    def reset(self) -> None:
        self.books.clear()
        self.members.clear()
        self.loans.clear()
        self._counters.clear()


store = Store()


def get_store() -> Store:
    return store


StoreDep = Annotated[Store, Depends(get_store)]
