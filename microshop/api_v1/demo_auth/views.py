import secrets
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Header,
)
from fastapi.security import (
    HTTPBasicCredentials,
    HTTPBasic,
)

router = APIRouter(
    prefix="/demo-auth",
    tags=["Demo Auth"],
)


user_basic_auth = HTTPBasic(
    scheme_name="Basic Auth",
    description="Your basic username and password auth  ",
    auto_error=False,
)


@router.get("/basic-auth/")
def demo_basic_auth_credentials(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(user_basic_auth),
    ],
):
    return {
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {
    "admin": "admin",
    "yaros": "qwerty",
}


static_auth_token_to_username = {
    "NfGKaG8w9riFZ0qeiR_50w": "admin",
    "I2-hTzrm9D29dEy-eRPexQ": "yaros",
}


def get_auth_user_username(
    credentials: Annotated[
        HTTPBasicCredentials,
        Depends(user_basic_auth),
    ],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_pwd = usernames_to_passwords.get(credentials.username, None)
    if correct_pwd is None:
        raise unauthed_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_pwd.encode("utf-8"),
    ):
        raise unauthed_exc
    return credentials.username


@router.get("/basic-auth-username/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {
        "message": f"Hi, {auth_username}!",
    }


def get_username_by_static_auth_token(
    api_token: str = Header(alias="x-auth-token"),
):
    if api_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    return static_auth_token_to_username[api_token]


@router.get("/some-http-header-auth/")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi, {username}!",
    }
