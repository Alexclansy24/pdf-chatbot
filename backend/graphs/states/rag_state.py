from typing import TypedDict


class RAGState(TypedDict):

    question: str

    context: str

    answer: str

    retrieved_chunks: int

    sources: list[dict]

    conversation_id: str | None

    chat_history: str | None