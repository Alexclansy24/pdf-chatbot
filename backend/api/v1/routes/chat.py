from fastapi import APIRouter

from schemas.chat import (
    ChatRequest,
)

from services.chat.service import (
    ChatService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post("")
async def chat(
    request: ChatRequest,
):

    service = ChatService()

    result = await service.ask(
        conversation_id=
            request.conversation_id,

        question=
            request.question,
    )

    return {
        "success": True,
        "data": result,
    }