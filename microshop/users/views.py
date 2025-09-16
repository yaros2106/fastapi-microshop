from fastapi import APIRouter

from users.schemas import CreateUser
from users.crud import create_user

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post("/")
def create_user_view(user: CreateUser) -> dict[str, bool | CreateUser]:
    return create_user(user_in=user)
