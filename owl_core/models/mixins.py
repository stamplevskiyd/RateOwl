from datetime import datetime
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[
    datetime, mapped_column(server_default=func.now(), onupdate=datetime.now)
]


class TimedMixin:
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
