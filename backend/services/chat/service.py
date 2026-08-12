from uuid import UUID

from services.graph.service import GraphService

from services.messages.repository import MessageRepository

from database.models.enums import MessageRole


class ChatService:

    def __init__(self):
        self.graph = GraphService()
        self.messages = MessageRepository()

    async def ask(
        self,
        conversation_id: UUID,
        document_id: UUID,
        question: str,
    ):

        # Save user message
        await self.messages.create(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=question,
        )

        # Ask Graph/RAG using the selected document
        result = await self.graph.ask(
            question=question,
            conversation_id=str(conversation_id),
            document_id=str(document_id),
        )

        # Save assistant response
        await self.messages.create(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=result["answer"],
        )

        return result