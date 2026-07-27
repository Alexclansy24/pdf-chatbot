from typing import TypedDict


class RAGState(TypedDict):

    question: str

    context: str

    answer: str

    retrieved_chunks: int

    sources: list[dict]