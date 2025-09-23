from asyncio import current_task
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import settings


class DatabaseHelper:
    def __init__(
        self,
        url: str,
        echo: bool = False,
    ):
        self.engine = create_async_engine(  # настройка движка
            url=url,
            echo=echo,
        )
        self.session_factory = async_sessionmaker(  # настройка сессии
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):  # создание сессии
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(
        self,
    ) -> AsyncGenerator[AsyncSession]:  # жизненный цикл конкретной сессии
        session = self.get_scoped_session()  # создать сессию
        async with session() as sess:  # отдать ее в роутер
            yield sess
            await session.remove()

    # async def session_dependency(self):
    #     session = self.get_scoped_session()
    #     yield session
    #     await session.close()


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
)
