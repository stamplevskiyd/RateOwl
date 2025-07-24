from abc import ABC, abstractmethod

from owl_core.db.base import Base


class BaseCommand(ABC):
    @abstractmethod
    async def validate(self) -> None:
        """Check if data is valid"""
        ...

    @abstractmethod
    async def run(self) -> Base:
        """Run action"""
        ...
