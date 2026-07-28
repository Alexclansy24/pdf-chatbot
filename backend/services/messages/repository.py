from uuid import UUID

from sqlalchemy import select

from database.session import AsyncSessionLocal

from database.models.message import (
    Message,
)

from database.models.enums import (
    MessageRole,
)


class MessageRepository:

    async def create(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str,
    ):

        async with AsyncSessionLocal() as session:

            message = Message(
                conversation_id=
                    conversation_id,
                role=role,
                content=content,
            )

            session.add(message)

            await session.commit()

            await session.refresh(
                message
            )

            return message

    async def history(
        self,
        conversation_id: UUID,
        limit: int = 20,
    ):

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(Message)
                .where(
                    Message.conversation_id
                    == conversation_id
                )
                .order_by(
                    Message.created_at.asc()
                )
                .limit(limit)
            )

            return (
                result.scalars().all()
            )