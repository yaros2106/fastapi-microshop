from datetime import datetime, UTC
from typing import TYPE_CHECKING

from sqlalchemy import func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base
from .order_product_association import order_product_association_table

if TYPE_CHECKING:
    from .product import ProductModel


class OrderModel(Base):
    __tablename__ = "orders"

    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=lambda: datetime.now(
            UTC
        ),  # lambda оборачивает вызов, чтобы SQLAlchemy мог сам вызывать её при вставке
    )
    products: Mapped[list["ProductModel"]] = relationship(
        secondary=order_product_association_table,
        back_populates="orders",
    )
