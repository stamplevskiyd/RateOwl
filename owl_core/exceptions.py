from typing import TypeVar, Type
from owl_core.db.base import Base
from fastapi import HTTPException

T = TypeVar("T", bound=Base)


class NotFoundException[T](HTTPException):
    def __init__(self, cls: Type[T]):
        super().__init__(
            status_code=404,
            detail=f"Object of {cls.__class__.__name__} class not found",
        )


class ForbiddenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Forbidden")
        pass
