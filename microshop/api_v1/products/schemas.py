from pydantic import BaseModel, ConfigDict
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


class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductCreateSchema(ProductBase):
    pass
