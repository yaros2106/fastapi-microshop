from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products.schemas import ProductCreateSchema
from core.models import ProductModel


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
