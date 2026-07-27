from typing import Generic, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(
        self,
        model: type[ModelType],
        db: AsyncSession,
    ):
        self.model = model
        self.db = db

    async def get_by_id(
        self,
        entity_id: UUID,
    ) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(
                self.model.id == entity_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        entity: ModelType,
    ) -> ModelType:
        self.db.add(entity)

        await self.db.commit()

        await self.db.refresh(entity)

        return entity

    async def delete(
        self,
        entity: ModelType,
    ) -> None:
        await self.db.delete(entity)

        await self.db.commit()