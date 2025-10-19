import secrets
from time import time
import uuid
from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Header,
    Response,
    Cookie,
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


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-cookie-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


@router.post("/login-cookie/")
def demo_auth_login_set_cookie(
    response: Response,
    # auth_username: str = Depends(get_auth_user_username),
    username: str = Depends(get_username_by_static_auth_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {
        "result": "ok!",
    }


def get_session_data(
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
) -> dict[str, Any]:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="not authenticated",
        )
    return COOKIES[session_id]


@router.get("/check-cookie/")
def demo_auth_check_cookie(
    user_session_data: dict[str, Any] = Depends(get_session_data),
):
    username = user_session_data["username"]
    return {
        "message": f"hello, {username}",
        **user_session_data,
    }


@router.get("/logout-cookie/")
def demo_auth_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict[str, Any] = Depends(get_session_data),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIE_SESSION_ID_KEY)
    username = user_session_data["username"]
    return {
        "message": f"Bye, {username}",
    }
