from datetime import date

from fastapi import APIRouter, HTTPException, status

from app.models import Member, MemberCreate
from app.storage import StoreDep

router = APIRouter(prefix="/members", tags=["members"])


@router.post("", response_model=Member, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate, store: StoreDep) -> Member:
    email = payload.email.strip().casefold()
    if any(m.email == email for m in store.members.values()):
        raise HTTPException(status.HTTP_409_CONFLICT, f"El correo {email} ya está registrado")
    member = Member(
        id=store.next_id("members"),
        name=payload.name,
        email=email,
        joined_at=date.today(),
    )
    store.members[member.id] = member
    return member


@router.get("", response_model=list[Member])
def list_members(store: StoreDep) -> list[Member]:
    return list(store.members.values())


@router.get("/{member_id}", response_model=Member)
def get_member(member_id: int, store: StoreDep) -> Member:
    member = store.members.get(member_id)
    if member is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Socio {member_id} no existe")
    return member
