from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from owl_core.db.base import Base
from owl_core.models.mixins.time_mixin import TimeMixin

if TYPE_CHECKING:
    from owl_core.models.reviews import Review
    from owl_core.models.titles import Title
    from owl_core.models.tags import Tag


class User(Base, TimeMixin):
    """User model"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str | None] = mapped_column()
    hashed_password: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="created_by",
        lazy="selectin",
        foreign_keys="Review.created_by_fk",
    )
    titles: Mapped[list["Title"]] = relationship(
        back_populates="created_by", lazy="selectin", foreign_keys="Title.created_by_fk"
    )
    tags: Mapped[list["Tag"]] = relationship(
        back_populates="created_by", lazy="selectin", foreign_keys="Tag.created_by_fk"
    )

    def __repr__(self) -> str:
        return f"<User({self.username})>"
