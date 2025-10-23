from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from pydantic import BaseModel

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    OAuth2PasswordBearer,
)
from jwt.exceptions import InvalidTokenError

from schemas.user_schema import UserSchema
from auth import utils_jwt


# http_bearer = HTTPBearer(
#     scheme_name="JWT",
#     description="Your **JWT token**",
#     auto_error=False,
# )
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-jwt/login",
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


router = APIRouter(
    prefix="/demo-jwt",
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
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not active",
        )
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


def get_current_token_payload(
    # credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    token: str = Depends(oauth2_scheme),
) -> dict:
    # token = credentials.credentials
    try:
        payload = utils_jwt.decode_jwt(token=token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"invalid token error",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="token invalid (user not found)",
    )


def get_current_active_user(
    user: UserSchema = Depends(get_current_auth_user),
) -> UserSchema:
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not active",
        )
    return user


@router.get("/users/me")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserSchema = Depends(get_current_active_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
