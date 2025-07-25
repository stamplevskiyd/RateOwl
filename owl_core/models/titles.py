from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from owl_core.db.base import Base
from owl_core.models.association_tables import tags_to_titles
from owl_core.models.mixins.audit_mixin import AuditMixin

from owl_core.models.tags import Tag

if TYPE_CHECKING:
    from owl_core.models.reviews import Review


class Title(Base, AuditMixin):
    """Model for movie/tv series/game/so on"""

    __tablename__ = "titles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    reviews: Mapped[list["Review"]] = relationship(
        back_populates="title", lazy="selectin"
    )
    tags: Mapped[list["Tag"]] = relationship(
        secondary=tags_to_titles, back_populates="titles", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Title({self.name})>"
