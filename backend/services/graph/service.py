from langsmith._openapi_client.types import run_select_field
from langsmith import traceable
from database.models.enums import MessageRole
import json
from uuid import UUID
from graphs.rag_graph import rag_graph

from services.retrieval.service import RetrievalService
from services.llm.streaming import stream_text
from services.messages.repository import MessageRepository

def _extract_text(content) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, str):
                    parts.append(block)
                elif isinstance(block, dict):
                    parts.append(block.get("text", ""))
            return "".join(parts)
        return ""

class GraphService:

    def __init__(self):
        self.retriever = RetrievalService()
        self.messages = MessageRepository()


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


    async def stream_pdf_answer(self, document_id, question, conversation_id, user_id):
        await self.messages.create(conversation_id=conversation_id, role=MessageRole.USER, content=question)

        state = {
            "question": question, "context": "", "answer": "",
            "retrieved_chunks": 0, "sources": [],
            "conversation_id": str(conversation_id), "document_id": document_id,
            "chat_history": "",
        }

        full_answer = ""
        sources = []

        async for event in rag_graph.astream_events(
            state, version="v2", config={"run_name": "pdf_rag_stream"}
        ):
            kind = event["event"]

            if kind == "on_chat_model_stream":
                token = _extract_text(event["data"]["chunk"].content)
                if token:
                    full_answer += token
                    yield {"type": "token", "data": token}

            elif kind == "on_chain_end" and event.get("name") == "retrieve":
                sources = event["data"]["output"].get("sources", [])

        await self.messages.create(conversation_id=conversation_id, role=MessageRole.ASSISTANT, content=full_answer)
        yield {"type": "sources", "data": sources}
        yield {"type": "done", "data": "complete"}