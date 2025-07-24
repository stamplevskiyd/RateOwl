from typing import TypeVar, get_args, Any

from sqlalchemy import select, BinaryExpression, Select
from sqlalchemy.ext.asyncio import AsyncSession

from owl_core.db.base import Base

T = TypeVar("T", bound=Base)


class BaseDAO[T]:
    """Base Data Access Object for CRUD operations."""

    """Model class for the DAO."""
    model_cls: type[T]
    base_filter: BinaryExpression | None = None
    check_access: bool = False

    def __init__(self, session: AsyncSession, user_id: int | None = None):
        self.session = session
        self.user_id = user_id

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
        return obj

    def base_select_query(self) -> Select:
        query = select(self.model_cls)
        if self.base_filter:
            query = query.where(*self.base_filter)
        return query

    async def find_by_id(self, pk: int) -> T | None:
        query = self.base_select_query().where(self.model_cls.id == pk)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_by_ids(self, ids: list[int]) -> list[T]:
        query = self.base_select_query().where(self.model_cls.id.in_(ids))  # type: ignore
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_all(self) -> list[T]:
        query = self.base_select_query()
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def find_one_filtered(self, filter_: BinaryExpression) -> T | None:
        query = self.base_select_query().where(filter_)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_by_id_filtered(self, pk: int, filter_: BinaryExpression) -> T | None:
        query = self.base_select_query().where(self.model_cls.id == pk).where(filter_)  # type: ignore
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def find_all_filtered(self, filter_: BinaryExpression) -> list[T]:
        query = self.base_select_query().where(filter_)
        result = await self.session.execute(query)
        return list(result.scalars().all())
