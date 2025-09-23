from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .base import Base


if TYPE_CHECKING:
    from .post import PostModel


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32), unique=True)
    posts: Mapped[list["PostModel"]] = relationship(back_populates="user")
