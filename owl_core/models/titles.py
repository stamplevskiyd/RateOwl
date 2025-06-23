from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from owl_core.db.base import Base
from owl_core.models.mixins import TimedMixin

if TYPE_CHECKING:
    from owl_core.models.reviews import Review


class Title(Base, TimedMixin):
    """Model for movie/tv series/game/so on"""

    __tablename__ = "titles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    slug: Mapped[str] = mapped_column(unique=True, index=True)
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="title", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Title({self.name})>"
