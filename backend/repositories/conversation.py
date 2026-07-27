from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.conversation import Conversation
from repositories.base import BaseRepository


class ConversationRepository(
    BaseRepository[Conversation]
):
    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            Conversation,
            db,
        )

    async def get_user_conversations(
        self,
        user_id: UUID,
    ) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.user_id == user_id
            )
        )

        return list(
            result.scalars().all()
        )