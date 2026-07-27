from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models.message import Message
from repositories.base import BaseRepository


class MessageRepository(
    BaseRepository[Message]
):
    def __init__(
        self,
        db: AsyncSession,
    ):
        super().__init__(
            Message,
            db,
        )

    async def get_conversation_messages(
        self,
        conversation_id: UUID,
    ) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(
                Message.conversation_id
                == conversation_id
            )
            .order_by(
                Message.created_at.asc()
            )
        )

        return list(
            result.scalars().all()
        )