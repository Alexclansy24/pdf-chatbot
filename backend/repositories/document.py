from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.document import Document
from repositories.base import BaseRepository


class DocumentRepository(
    BaseRepository[Document]
):
    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            Document,
            db,
        )

    async def get_user_documents(
        self,
        user_id: UUID,
    ) -> list[Document]:
        result = await self.db.execute(
            select(Document)
            .where(
                Document.user_id == user_id
            )
        )

        return list(
            result.scalars().all()
        )