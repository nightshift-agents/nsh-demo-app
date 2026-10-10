from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, status

from app.models import Loan, LoanCreate
from app.storage import Store, StoreDep

router = APIRouter(prefix="/loans", tags=["loans"])

DEFAULT_LOAN_DAYS = 14
MAX_ACTIVE_LOANS_PER_MEMBER = 3


def _get_loan_or_404(loan_id: int, store: Store) -> Loan:
    loan = store.loans.get(loan_id)
    if loan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Préstamo {loan_id} no existe")
    return loan


@router.post("", response_model=Loan, status_code=status.HTTP_201_CREATED)
def create_loan(payload: LoanCreate, store: StoreDep) -> Loan:
    if payload.book_id not in store.books:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Libro {payload.book_id} no existe")
    if payload.member_id not in store.members:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Socio {payload.member_id} no existe")

    # Verificar que el libro no esté ya prestado
    active_for_book = [
        loan for loan in store.loans.values() if loan.book_id == payload.book_id and loan.is_active
    ]
    if active_for_book:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"El libro {payload.book_id} ya está prestado",
        )

    active_for_member = [
        loan
        for loan in store.loans.values()
        if loan.member_id == payload.member_id and loan.is_active
    ]
    if len(active_for_member) >= MAX_ACTIVE_LOANS_PER_MEMBER:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            f"El socio ya tiene {MAX_ACTIVE_LOANS_PER_MEMBER} préstamos activos",
        )

    today = date.today()
    loan = Loan(
        id=store.next_id("loans"),
        book_id=payload.book_id,
        member_id=payload.member_id,
        loaned_at=today,
        due_date=payload.due_date or today + timedelta(days=DEFAULT_LOAN_DAYS),
    )
    store.loans[loan.id] = loan
    return loan


@router.get("", response_model=list[Loan])
def list_loans(
    store: StoreDep,
    member_id: int | None = None,
    active: bool | None = None,
) -> list[Loan]:
    loans = list(store.loans.values())
    if member_id is not None:
        loans = [loan for loan in loans if loan.member_id == member_id]
    if active is not None:
        loans = [loan for loan in loans if loan.is_active == active]
    return loans


@router.get("/{loan_id}", response_model=Loan)
def get_loan(loan_id: int, store: StoreDep) -> Loan:
    return _get_loan_or_404(loan_id, store)


@router.post("/{loan_id}/return", response_model=Loan)
def return_loan(loan_id: int, store: StoreDep) -> Loan:
    loan = _get_loan_or_404(loan_id, store)
    if not loan.is_active:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Préstamo {loan_id} ya fue devuelto")
    loan.returned_at = date.today()
    return loan
