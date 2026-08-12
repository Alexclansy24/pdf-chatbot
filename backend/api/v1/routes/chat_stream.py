import json
from fastapi.responses import StreamingResponse
from uuid import UUID
from asyncio import sleep

from fastapi import (
    APIRouter,
    Depends,
)

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
from services.auth.dependencies import (
    get_current_user,
)
from database.models.user import User

router = APIRouter(
    prefix="/chat-stream",
    tags=["Chat Stream"],
)



class StreamRequest(
    BaseModel
):
    document_id: UUID
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

@router.post("/tokens")
async def token_stream(
    request: StreamRequest,
    current_user: User = Depends(get_current_user),
):
    service = GraphService()

    async def event_generator():

        async for event in service.stream_pdf_answer(
            document_id=request.document_id,
            question=request.question,
            user_id=current_user.id,
        ):

            event_type = event["type"]

            # -------------------------
            # TOKEN
            # -------------------------

            if event_type == "token":

                yield (
                    "event: token\n"
                    f"data: {json.dumps(event['data'])}\n\n"
                )

            # -------------------------
            # SOURCES
            # -------------------------

            elif event_type == "sources":

                yield (
                    "event: sources\n"
                    f"data: {json.dumps(event['data'])}\n\n"
                )

        # -------------------------
        # DONE
        # -------------------------

        yield (
            "event: done\n"
            "data: complete\n\n"
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )