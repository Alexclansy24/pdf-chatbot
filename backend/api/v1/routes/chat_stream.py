from asyncio import sleep

from fastapi import APIRouter

from sse_starlette.sse import (
    EventSourceResponse,
)
from services.graph.service import (
    GraphService,
)
from pydantic import BaseModel

from services.llm.streaming import (
    stream_text,
)

router = APIRouter(
    prefix="/chat-stream",
    tags=["Chat Stream"],
)



class StreamRequest(
    BaseModel
):
    question: str

async def graph_stream(
    question: str,
):
    service = GraphService()

    async for event in service.stream_answer(
        question
    ):

        yield {
            "event": "graph",
            "data": str(event),
        }

    yield {
        "event": "done",
        "data": "complete",
    }

@router.post("")
async def stream_chat(
    request: StreamRequest,
):
    return EventSourceResponse(
        graph_stream(
            request.question
        )
    )

@router.get("/tokens")
async def token_stream(
    question: str,
):

    async for token in stream_text(
        question
    ):

        yield {
            "event": "token",
            "data": token,
        }

    yield {
        "event": "done",
        "data": "complete",
    }