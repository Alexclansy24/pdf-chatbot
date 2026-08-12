import json
from uuid import UUID
from graphs.rag_graph import rag_graph

from services.retrieval.service import RetrievalService
from services.llm.streaming import stream_text


class GraphService:

    def __init__(self):
        self.retriever = RetrievalService()

    async def ask(
        self,
        question: str,
        conversation_id: str | None = None,
        document_id: str | None = None,
    ):

        result = await rag_graph.ainvoke(
            {
                "question": question,
                "context": "",
                "answer": "",
                "retrieved_chunks": 0,
                "sources": [],
                "conversation_id": conversation_id,
                "document_id": document_id,
                "chat_history": "",
            }
        )

        return result

    async def stream_answer(
        self,
        question: str,
        conversation_id: str | None = None,
        document_id: str | None = None,
    ):

        state = {
            "question": question,
            "context": "",
            "answer": "",
            "retrieved_chunks": 0,
            "sources": [],
            "conversation_id": conversation_id,
            "document_id": document_id,
            "chat_history": "",
        }

        async for event in rag_graph.astream(state):
            yield event

    async def stream_pdf_answer(
    self,
    document_id: str,
    question: str,
    user_id: UUID,
    ):
        results = await self.retriever.retrieve(
            query=question,
            limit=5,
            document_id=document_id,
        )

        contexts = []
        sources = []

        for point in results.points:
            payload = point.payload

            contexts.append(
                payload.get("content", "")
            )

        sources.append(
            {
                "document_id": payload.get(
                    "document_id"
                ),
                "chunk_id": payload.get(
                    "chunk_id"
                ),
                "chunk_index": payload.get(
                    "chunk_index"
                ),
                "score": point.score,
            }
        )

        context = "\n\n".join(contexts)

        if not contexts:
            yield {
                "event": "token",
                "data": (
                    "I could not find relevant "
                    "information in the uploaded document."
                ),
            }

            yield {
                "event": "done",
                "data": "complete",
            }

            return

        prompt = f"""
        You are a PDF assistant.

        Answer ONLY using the provided context.

        If the answer is not present in the context,
        say that you could not find the information
        in the uploaded document.

        Context:
        {context}

        Question:
        {question}
        """

        async for token in stream_text(prompt):
            yield {
                "type": "token",
                "data": token,
            }

        yield {
            "type": "sources",
            "data": sources,
        }

        yield {
            "type": "done",
            "data": "complete",
        }