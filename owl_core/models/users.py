from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from owl_core.db.base import Base
from owl_core.models.mixins import TimedMixin

if TYPE_CHECKING:
    from owl_core.models.reviews import Review


class User(Base, TimedMixin):
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
        back_populates="author", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<User({self.username})>"
