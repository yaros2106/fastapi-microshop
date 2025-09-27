from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    UniqueConstraint,
)
from models import Base

order_product_association_table = Table(
    "order_product_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", ForeignKey("orders.id"), nullable=False),
    Column("product_id", ForeignKey("products.id"), nullable=False),
    UniqueConstraint("order_id", "product_id", name="order_product_association_unique"),
)
