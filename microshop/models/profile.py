from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class ProfileModel(UserRelationMixin, Base):
    __tablename__ = "profiles"

    _user_id_is_unique = True
    _back_populates = "profile"

    first_name: Mapped[str | None] = mapped_column(String(40))
    last_name: Mapped[str | None] = mapped_column(String(40))
    biography: Mapped[str | None] = mapped_column(Text)
