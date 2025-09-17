from pydantic import BaseModel
from typing import Annotated
from annotated_types import MinLen, MaxLen


class ProductBase(BaseModel):
    name: Annotated[
        str,
        MinLen(3),
        MaxLen(25),
    ]
    description: str
    price: int


class Product(ProductBase):
    id: int


class ProductCreate(ProductBase):
    pass
