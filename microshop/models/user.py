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
    from .profile import ProfileModel


class UserModel(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32), unique=True)

    posts: Mapped[list["PostModel"]] = relationship(back_populates="user")
    profile: Mapped["ProfileModel"] = relationship(back_populates="user", uselist=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)
