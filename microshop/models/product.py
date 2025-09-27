from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, relationship

from .base import Base
from .order_product_association import order_product_association_table


if TYPE_CHECKING:
    from .order import OrderModel


class ProductModel(Base):
    __tablename__ = "products"

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]

    orders: Mapped[list["OrderModel"]] = relationship(
        secondary=order_product_association_table,
        back_populates="products",
    )
