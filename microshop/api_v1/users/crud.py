from schemas.user_schema import CreateUser


def create_user(user_in: CreateUser) -> dict[str, bool | CreateUser]:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
