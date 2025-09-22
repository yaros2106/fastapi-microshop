from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PostModel(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",  # python-level default
        server_default="",  # db-level default
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
