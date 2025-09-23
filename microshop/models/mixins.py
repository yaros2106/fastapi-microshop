from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)


if TYPE_CHECKING:
    from .user import UserModel


class UserRelationMixin:
    _user_id_nullable: bool = False
    _user_id_is_unique: bool = False
    _back_populates: str | None = None

    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            unique=cls._user_id_is_unique,
            nullable=cls._user_id_nullable,
        )

    # user: Mapped["UserModel"] = relationship(back_populates="profile")

    @declared_attr
    def user(cls) -> Mapped["UserModel"]:
        return relationship(
            "UserModel",
            back_populates=cls._back_populates,
        )
