from fastapi import (
    APIRouter,
    Depends,
)
from pydantic import BaseModel

from fastapi.security import (
    HTTPBearer,
)

from api_v1.demo_auth.helpers import (
    create_access_token,
    create_refresh_token,
)
from api_v1.demo_auth.validation import (
    get_current_token_payload,
    get_current_auth_user_for_refresh,
    validate_auth_user,
    get_current_active_user,
)
from schemas.user_schema import UserSchema

http_bearer = HTTPBearer(
    scheme_name="JWT",
    description="Your **JWT token**",
    auto_error=False,
)


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


router = APIRouter(
    prefix="/demo-jwt",
    tags=["JWT"],
    dependencies=[Depends(http_bearer)],
)


@router.post(
    "/login",
    response_model=TokenInfo,
)
def auth_user_issue_jwt(
    user: UserSchema = Depends(validate_auth_user),
):
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


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


@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
def auth_user_refresh_jwt(
    user: UserSchema = Depends(get_current_auth_user_for_refresh),
):
    access_token = create_access_token(user=user)
    return TokenInfo(access_token=access_token)
