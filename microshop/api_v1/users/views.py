from fastapi import APIRouter

from api_v1.users.schemas import CreateUser
from api_v1.users.crud import create_user

router = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router.post("/")
def create_user_view(user: CreateUser) -> dict[str, bool | CreateUser]:
    return create_user(user_in=user)
