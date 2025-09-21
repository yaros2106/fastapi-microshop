from fastapi import Depends, status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from api_v1.products.dependencies import prefetch_product
from schemas.product_schema import (
    ProductSchema,
    ProductUpdateSchema,
    ProductUpdatePartialSchema,
)
from models import ProductModel, db_helper


router = APIRouter(
    prefix="/{product_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Product not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Product with id 'some-id' not found",
                    },
                },
            },
        },
    },
)


@router.get(
    "/",
    response_model=ProductSchema,
)
async def get_product_by_id_view(
    product: ProductModel = Depends(prefetch_product),
) -> ProductModel:
    return product


@router.put(
    "/",
    response_model=ProductSchema,
)
async def update_product_view(
    product_update: ProductUpdateSchema,
    product: ProductModel = Depends(prefetch_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProductModel:
    return await crud.update_product(
        product=product,
        product_update=product_update,
        session=session,
    )


@router.patch(
    "/",
    response_model=ProductSchema,
)
async def update_partial_product_view(
    product_update_partial: ProductUpdatePartialSchema,
    product: ProductModel = Depends(prefetch_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProductModel:
    return await crud.update_product(
        product=product,
        product_update=product_update_partial,
        session=session,
        partial=True,
    )


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_product_view(
    product: ProductModel = Depends(prefetch_product),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    return await crud.delete_product(
        product=product,
        session=session,
    )
