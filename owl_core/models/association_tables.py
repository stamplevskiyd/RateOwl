from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey

from owl_core.db.base import Base

tags_to_titles = Table(
    "tags_to_titles",
    Base.metadata,
    Column("tag_id", ForeignKey("tags.id")),
    Column("title_id", ForeignKey("titles.id")),
)
