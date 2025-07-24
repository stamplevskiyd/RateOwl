from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import declared_attr, relationship, Mapped, mapped_column

from owl_core.context import current_user_id
from owl_core.models.mixins.time_mixin import TimeMixin


class AuditMixin(TimeMixin):
    @declared_attr
    def created_by_fk(cls) -> Mapped[int]:
        return mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            default=lambda: current_user_id.get(),
        )

    @declared_attr
    def created_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.created_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
            lazy="selectin",
        )

    @declared_attr
    def changed_by_fk(cls) -> Mapped[int]:
        return mapped_column(
            Integer,
            ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            default=lambda: current_user_id.get(),
            onupdate=lambda: current_user_id.get(),
        )

    @declared_attr
    def changed_by(cls):
        return relationship(
            "User",
            primaryjoin="%s.changed_by_fk == User.id" % cls.__name__,
            enable_typechecks=False,
            lazy="selectin",
        )
