from auth import utils_jwt
from schemas.user_schema import UserSchema

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
