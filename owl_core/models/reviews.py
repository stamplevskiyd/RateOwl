from sqlalchemy.orm import Mapped, mapped_column

from owl_core.db.base import Base
from owl_core.models.mixins import TimedMixin


class Review(Base, TimedMixin):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    rate: Mapped[int]
