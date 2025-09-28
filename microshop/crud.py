import asyncio

from sqlalchemy import select

from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

from models import (
    db_helper,
    UserModel,
    ProductModel,
    PostModel,
    ProfileModel,
    OrderModel,
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


async def show_users_with_profiles(session: AsyncSession) -> None:
    stmt = (
        select(UserModel).options(joinedload(UserModel.profile)).order_by(UserModel.id)
    )  # joinedload - one-to-one
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:
        print(user)
        print(user.profile)


async def create_posts(
    session: AsyncSession,
    user_id: int,
    *post_titles: str,
) -> list[PostModel]:
    posts = [PostModel(user_id=user_id, title=title) for title in post_titles]
    session.add_all(posts)
    await session.commit()
    print("posts:", posts)
    return posts


async def get_users_with_posts(session: AsyncSession):
    # stmt = select(UserModel).options(joinedload(UserModel.posts)).order_by(UserModel.id)
    stmt = (
        select(UserModel).options(selectinload(UserModel.posts)).order_by(UserModel.id)
    )  # selectinload - one-to-many
    # users = await session.scalars(stmt)
    result: Result = await session.execute(stmt)
    # users = result.unique().scalars()
    users = result.scalars()
    for user in users:
        print("****" * 10)
        print(user)
        for post in user.posts:
            print("-", post)


async def get_posts_with_authors(session: AsyncSession):
    stmt = select(PostModel).options(joinedload(PostModel.user)).order_by(PostModel.id)
    result: Result = await session.execute(stmt)
    posts = result.scalars()
    for post in posts:
        print("****" * 10)
        print("post:", post)
        print("author:", post.user.username)


async def get_users_with_posts_and_profile(session: AsyncSession):
    stmt = (
        select(UserModel)
        .options(
            selectinload(UserModel.posts),
            joinedload(UserModel.profile),
        )
        .order_by(UserModel.id)
    )
    result: Result = await session.execute(stmt)
    users = result.scalars()
    for user in users:
        print("****" * 10)
        print("user:", user)
        print(
            "profile:", user.profile and user.profile.first_name
        )  # если есть профиль, находится first_name, иначе до 'user.profile.first_name' не доходит и будет None
        for post in user.posts:
            print("-", post)


async def get_profiles_with_users_and_user_with_posts(session: AsyncSession):
    # stmt = (
    #     select(ProfileModel)
    #     .join(ProfileModel.user)
    #     .options(
    #         joinedload(ProfileModel.user).selectinload(UserModel.posts),
    #     )
    #     .where(UserModel.username == "yaros")
    #     .order_by(ProfileModel.id)
    # )
    stmt = (
        select(ProfileModel)
        .join(ProfileModel.user)  # SQL join — нужно для фильтрации по users.username
        .options(
            contains_eager(  # заполнить ProfileModel.user из join
                ProfileModel.user
            ).selectinload(  # затем подгрузить posts отдельным запросом
                UserModel.posts
            ),
        )  # contains_eager - использует результат уже сделанного join
        .where(UserModel.username == "yaros")
        .order_by(ProfileModel.id)
    )
    result: Result = await session.execute(stmt)
    profiles = result.scalars()
    for profile in profiles:
        print("****" * 10)
        print("profile:", profile)
        print("user:", profile.user.username)
        for post in profile.user.posts:
            print("-", post)


async def main_relations(session: AsyncSession):
    # await create_user(session=session, username="olya")
    # await create_user(session=session, username="alice")
    # user_yaros = await get_user_by_username(session=session, username="yaros")
    # user_max = await get_user_by_username(session=session, username="max")
    # user_alice = await get_user_by_username(session=session, username="alice")
    # await create_user_profile(
    #     session=session,
    #     user_id=user_alice.id,
    #     first_name="Sam",
    #     last_name="S",
    # )
    # await create_user_profile(
    #     user_id=user_dan.id,
    #     session=session,
    #     first_name="Dan",
    #     last_name="D",
    # )
    # await show_users_with_profiles(session=session)
    # await create_posts(
    #     session,
    #     user_yaros.id,
    #     "SQL 2.0",
    #     "SQL Joins",
    # )
    #
    # await create_posts(
    #     session,
    #     user_max.id,
    #     "Fastapi Intro",
    #     "Fastapi Advanced",
    #     "Fastapi more",
    # )
    # await get_users_with_posts(session=session)
    # await get_posts_with_authors(session=session)
    # await get_users_with_posts_and_profile(session=session)
    await get_profiles_with_users_and_user_with_posts(session=session)


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> OrderModel:
    order = OrderModel(promocode=promocode)
    session.add(order)
    await session.commit()
    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> ProductModel:
    product = ProductModel(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def create_orders_and_products(session: AsyncSession):
    order_one = await create_order(session=session)
    order_promo = await create_order(session=session, promocode="promo")
    mouse = await create_product(
        session=session,
        name="Mouse",
        description="Gaming mouse",
        price=100,
    )
    keyboard = await create_product(
        session=session,
        name="Keyboard",
        description="Gaming keyboard",
        price=150,
    )
    display = await create_product(
        session=session,
        name="Display",
        description="Gaming display",
        price=299,
    )
    order_one = await get_order_by_id_with_products(
        session=session, order_id=order_one.id
    )
    order_promo = await get_order_by_id_with_products(
        session=session, order_id=order_promo.id
    )

    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    order_promo.products.append(keyboard)
    order_promo.products.append(display)

    await session.commit()


async def get_orders_with_products(session: AsyncSession):
    stmt = (
        select(OrderModel)
        .options(selectinload(OrderModel.products))
        .order_by(OrderModel.id)
    )
    result: Result = await session.execute(stmt)
    orders = result.scalars()
    for order in orders:
        print("****" * 10)
        print("order_id:", order.id)
        for product in order.products:  # type: ProductModel
            print("- product:", product.name)


async def get_order_by_id_with_products(
    session: AsyncSession, order_id: int
) -> OrderModel:
    stmt = (
        select(OrderModel)
        .options(selectinload(OrderModel.products))
        .where(OrderModel.id == order_id)
    )
    result: Result = await session.execute(stmt)
    order = result.scalar()
    return order


async def demo_m2m(session: AsyncSession):
    # await create_orders_and_products(session=session)
    await get_orders_with_products(session=session)


async def main():
    async with db_helper.session_factory() as session:
        # await main_relations(session=session)
        await demo_m2m(session=session)


if __name__ == "__main__":
    asyncio.run(main())
