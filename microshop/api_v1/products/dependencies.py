from fastapi import (
    Path,
    Depends,
    status,
    HTTPException,
)
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.products import crud
from core.models import (
    db_helper,
    ProductModel,
)


async def prefetch_product(
    product_id: Annotated[int, Path(description="Product ID")],
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> ProductModel:
    product = await crud.get_product_by_id(
        session=session,
        product_id=product_id,
    )
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product with id:{product_id} not found",
    )
