from datetime import datetime, UTC

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrderModel(Base):
    __tablename__ = "orders"

    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        default=lambda: datetime.now(
            UTC
        ),  # lambda оборачивает вызов, чтобы SQLAlchemy мог сам вызывать её при вставке
    )
