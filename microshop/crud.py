import asyncio
from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    db_helper,
    UserModel,
    ProductModel,
    PostModel,
    ProfileModel,
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
    # result: Result = await session.execute(stmt)
    # user: UserModel | None = result.scalar_one_or_none()
    user: UserModel | None = await session.scalar(stmt)
    print("found user:", username, user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None,
    last_name: str | None,
    biography: str | None = None,
) -> ProfileModel:
    profile = ProfileModel(
        user_id=user_id,
        first_name=first_name,
        last_name=last_name,
        biography=biography,
    )
    session.add(profile)
    await session.commit()
    return profile


async def main():
    async with db_helper.session_factory() as session:
        # await create_user(session=session, username="dan")
        user_yaros = await get_user_by_username(session=session, username="yaros")
        user_max = await get_user_by_username(session=session, username="max")
        await create_user_profile(
            session=session,
            user_id=user_yaros.id,
            first_name="Yaros",
            last_name="Bereza",
        )
        await create_user_profile(
            session=session,
            user_id=user_max.id,
            first_name="Max",
            last_name="Smith",
        )


if __name__ == "__main__":
    asyncio.run(main())
