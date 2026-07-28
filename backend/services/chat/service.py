from langsmith._openapi_client.types import run_select_field
from uuid import UUID

from services.graph.service import (
    GraphService,
)

from services.messages.repository import (
    MessageRepository,
)

from database.models.enums import (
    MessageRole,
)


class ChatService:

    def __init__(self):

        self.graph = GraphService()

        self.messages = (
            MessageRepository()
        )
    
    async def ask(
        self,
        conversation_id: UUID,
        question: str,
    ):

        await self.messages.create(
            conversation_id=
                conversation_id,

            role=MessageRole.USER,

            content=question,
        )

        result = await self.graph.ask(
            question=question,
            conversation_id=str(
                    conversation_id
                ),
            )

        await self.messages.create(
            conversation_id=
                conversation_id,

            role=MessageRole.ASSISTANT,

            content=result["answer"],
        )

        return result
