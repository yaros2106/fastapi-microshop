import asyncio
from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    db_helper,
    UserModel,
    ProductModel,
    PostModel,
)


async def create_user(
    session: AsyncSession,
    username: str,
) -> UserModel:
    user = UserModel(username=username)
    session.add(user)
    await session.commit()
    print("user:", user)
    return user


async def get_user_by_username(
    session: AsyncSession,
    username: str,
) -> UserModel | None:
    stmt = select(UserModel).where(UserModel.username == username)
    result: Result = await session.execute(stmt)
    user: UserModel | None = result.scalar_one_or_none()
    print("found user:", username, user)
    return user


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="dan")
        await get_user_by_username(session=session, username="yaros")
        await get_user_by_username(session=session, username="bob")


if __name__ == "__main__":
    asyncio.run(main())
