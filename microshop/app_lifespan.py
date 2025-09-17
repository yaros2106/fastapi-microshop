from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.models import Base, db_helper


@asynccontextmanager
async def lifespan(
    app: FastAPI,  # noqa: ARG001
) -> AsyncGenerator[None]:
    # действие до запуска приложения
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # ставим эту функцию на паузу на время работы приложения
    yield
    # выполняем завершение работы,
    # закрываем соединение, финально все сохраняем
