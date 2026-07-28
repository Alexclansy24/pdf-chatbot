from uuid import UUID

from pydantic import BaseModel


class ChatRequest(BaseModel):

    conversation_id: UUID

    question: str