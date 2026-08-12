from pydantic import BaseModel
from uuid import UUID


class ChatRequest(BaseModel):
    conversation_id: UUID
    document_id: UUID
    question: str