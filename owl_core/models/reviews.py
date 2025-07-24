from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from owl_core.db.base import Base
from owl_core.models.mixins.audit_mixin import AuditMixin

if TYPE_CHECKING:
    from owl_core.models.titles import Title
    from owl_core.models.tags import Tag


class Review(Base, AuditMixin):
    """Review model"""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    text: Mapped[str] = mapped_column(Text)
    rate: Mapped[int]
    title_id: Mapped[int] = mapped_column(ForeignKey("titles.id", ondelete="SET NULL"))
    title: Mapped["Title"] = relationship(back_populates="reviews", lazy="selectin")
    hidden: Mapped[bool] = mapped_column(default=False, server_default="false")

    # def __repr__(self) -> str:
    #     return f"<Review({self.description})>"

    @property
    def tags(self) -> list["Tag"]:
        return self.title.tags
