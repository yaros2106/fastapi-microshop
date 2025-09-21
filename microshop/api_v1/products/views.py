from fastapi import (
    APIRouter,
    HTTPException,
    status,
    Depends,
)
from watchfiles import awatch

from core.models import db_helper
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.schemas import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)
from api_v1.products.dependencies import prefetch_product
from core.models import ProductModel

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
)
async def create_product_view(
    product: ProductCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProductModel:
    return await crud.create_product(product_in=product, session=session)


@router.get(
    "/{product_id}",
    response_model=ProductSchema,
)
async def get_product_view(
    product: ProductModel = Depends(prefetch_product),
) -> ProductModel:
    return product


@router.put(
    "/{product_id}",
    response_model=ProductSchema,
)
async def update_product_view(
    product_update: ProductUpdateSchema,
    product: ProductModel = Depends(prefetch_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    return await crud.update_product(
        product=product,
        product_update=product_update,
        session=session,
    )
