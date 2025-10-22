from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)

from pydantic import BaseModel
from schemas.user_schema import UserSchema
from auth import utils_jwt


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(
    prefix="/jwt",
    tags=["JWT"],
)


john = UserSchema(
    username="john",
    password=utils_jwt.hash_password("qwerty"),
    email="john@example.com",
)

sam = UserSchema(
    username="sam",
    password=utils_jwt.hash_password("secret"),
)

users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid username or password",
    )
    if not (user := users_db.get(username)):
        raise unauthed_exc
    if utils_jwt.validate_password(
        password=password,
        hashed_password=user.password,
    ):
        return user
    raise unauthed_exc


@router.post(
    "/login",
    response_model=TokenInfo,
)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    jwt_payload = {
        # subject
        "sub": user.username,  # в sub лучше всего класть, например id, если он есть
        "username": user.username,
        "email": user.email,
    }
    token = utils_jwt.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )
