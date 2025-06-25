from typing import TypeVar, get_args, Any

from sqlalchemy import select, BinaryExpression
from sqlalchemy.ext.asyncio import AsyncSession

from owl_core.db.base import Base

T = TypeVar("T", bound=Base)


class BaseDAO[T]:
    """Base Data Access Object for CRUD operations."""

    """Model class for the DAO."""
    model_cls: type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

        # Get class from type hints
        self.model_cls = get_args(
            self.__class__.__orig_bases__[0]  # type: ignore
        )[0]

    async def create(self, data: dict[str, Any], commit: bool = True) -> T:
        new_obj = self.model_cls(**data)
        self.session.add(new_obj)
        if commit:
            await self.session.commit()
        await self.session.refresh(new_obj)
        return new_obj

    async def update(self, obj: T, data: dict[str, Any], commit: bool = True) -> T:
        for key, value in data.items():
            setattr(obj, key, value)
        if commit:
            await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: T, commit: bool = True) -> T:
        await self.session.delete(obj)
        if commit:
            await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def find_by_id(self, pk: int) -> T | None:
        query = select(self.model_cls).where(self.model_cls.id == pk)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_by_ids(self, ids: list[int]) -> list[T]:
        query = select(self.model_cls).where(self.model_cls.id.in_(ids))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_all(self) -> list[T]:
        query = select(self.model_cls)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_one_filtered(self, *filters: BinaryExpression) -> T | None:
        query = select(self.model_cls)
        if filters:
            query = query.where(*filters)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_all_filtered(self, *filters: BinaryExpression) -> list[T]:
        query = select(self.model_cls)
        if filters:
            query = query.where(*filters)
        result = await self.session.execute(query)
        return list(result.scalars().all())
