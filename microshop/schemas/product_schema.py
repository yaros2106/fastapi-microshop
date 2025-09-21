from pydantic import BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MinLen, MaxLen


NameString = Annotated[
    str,
    MinLen(3),
    MaxLen(25),
]


class ProductBase(BaseModel):
    name: NameString
    description: str
    price: int


class ProductSchema(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ProductCreateSchema(ProductBase):
    pass


class ProductUpdateSchema(ProductCreateSchema):
    pass


class ProductUpdatePartialSchema(BaseModel):
    name: NameString | None = None
    description: str | None = None
    price: int | None = None
