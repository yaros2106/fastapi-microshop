from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.product_schema import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductUpdatePartialSchema,
)
from models import ProductModel


async def get_products(session: AsyncSession) -> list[ProductModel]:
    stmt = select(ProductModel).order_by(ProductModel.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product_by_id(
    session: AsyncSession,
    product_id: int,
) -> ProductModel | None:
    return await session.get(ProductModel, product_id)


async def create_product(
    session: AsyncSession, product_in: ProductCreateSchema
) -> ProductModel:
    product = ProductModel(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh(product)
    return product


async def update_product(
    product: ProductModel,
    product_update: ProductUpdateSchema | ProductUpdatePartialSchema,
    session: AsyncSession,
    partial: bool = False,
) -> ProductModel:
    for field_name, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, field_name, value)
    await session.commit()
    return product


async def delete_product(
    product: ProductModel,
    session: AsyncSession,
) -> None:
    await session.delete(product)
    await session.commit()
