from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api_v1.products import crud
from api_v1.products.schemas import ProductSchema, ProductCreateSchema
from core.models import db_helper, ProductModel


from fastapi import (
    APIRouter,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get(
    "/",
    response_model=list[ProductSchema],
)
async def get_products_view(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ProductModel]:
    return await crud.get_products(session=session)


@router.post(
    "/",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_product_view(
    product: ProductCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProductModel:
    return await crud.create_product(product_in=product, session=session)
