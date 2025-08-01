from typing import TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship

from owl_core.db.base import Base
from owl_core.models.association_tables import tags_to_titles
from owl_core.models.mixins.audit_mixin import AuditMixin

if TYPE_CHECKING:
    from owl_core.models.titles import Title


class Tag(Base, AuditMixin):
    """Model for review tag (media type)"""

    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(index=True)
    titles: Mapped[list["Title"]] = relationship(
        secondary=tags_to_titles, back_populates="tags", lazy="selectin"
    )
