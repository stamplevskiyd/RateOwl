from abc import ABC, abstractmethod
from typing import TypeVar

from owl_core.db.base import Base

T = TypeVar("T", bound=Base)


class BaseCommand(ABC):
    @abstractmethod
    async def validate(self) -> None:
        """Check if data is valid"""
        ...

    @abstractmethod
    async def run(self) -> T:
        """Run action"""
        ...
