from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from models import Base


if TYPE_CHECKING:
    from .order import OrderModel
    from .product import ProductModel


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (
        UniqueConstraint(
            "order_id", "product_id", name="order_product_association_unique"
        ),
    )

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1, server_default="1")
    unit_price: Mapped[int] = mapped_column(default=0, server_default="0")

    # association between Assocation -> OrderModel
    order: Mapped["OrderModel"] = relationship(
        back_populates="products_associations",
    )
    # association between Assocation -> ProductModel
    product: Mapped["ProductModel"] = relationship(
        back_populates="orders_associations",
    )
