from fastapi import Depends, HTTPException, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from api_v1.demo_auth.crud import users_db
from api_v1.demo_auth.helpers import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from auth import utils_jwt
from schemas.user_schema import UserSchema


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/demo-jwt/login",
)


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


def validate_token_type(payload: dict, token_type: str) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail=f"invalid token type {current_token_type!r} when expected {token_type!r}",
    )


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(
        payload=payload,
        token_type=ACCESS_TOKEN_TYPE,
    )
    return get_user_by_token_subject(payload=payload)


def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    validate_token_type(
        payload=payload,
        token_type=REFRESH_TOKEN_TYPE,
    )
    return get_user_by_token_subject(payload=payload)


def get_current_active_user(
    user: UserSchema = Depends(get_current_auth_user),
) -> UserSchema:
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not active",
        )
    return user


def get_user_by_token_subject(payload: dict) -> UserSchema:
    username: str | None = payload.get("sub")
    if user := users_db.get(username):
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="token invalid (user not found)",
    )
