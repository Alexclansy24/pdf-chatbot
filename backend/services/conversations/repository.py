from uuid import UUID

from sqlalchemy import select

from database.session import AsyncSessionLocal
from database.models.conversation import (
    Conversation,
)


class ConversationRepository:

    async def create(
        self,
        user_id: UUID,
        title: str = "New Conversation",
    ):

        async with AsyncSessionLocal() as session:

            conversation = Conversation(
                user_id=user_id,
                title=title,
            )

            session.add(conversation)

            await session.commit()

            await session.refresh(
                conversation
            )

            return conversation

    async def get(
        self,
        conversation_id: UUID,
        user_id: UUID,
    ):

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id,
                )
            )

            return (
                result.scalar_one_or_none()
            )

    async def list_by_user(
        self,
        user_id: UUID,
    ):

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(Conversation)
                .where(
                    Conversation.user_id
                    == user_id
                )
                .order_by(
                    Conversation.created_at.desc()
                )
            )

            return (
                result.scalars().all()
            )