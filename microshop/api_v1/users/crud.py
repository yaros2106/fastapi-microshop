from api_v1.users.schemas import CreateUser


def create_user(user_in: CreateUser) -> dict[str, bool | CreateUser]:
    user = user_in.model_dump()
    return {
        "success": True,
        "user": user,
    }
