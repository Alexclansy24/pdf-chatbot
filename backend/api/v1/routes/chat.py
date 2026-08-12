from fastapi import APIRouter

from schemas.chat import (
    ChatRequest,
)

from services.chat.service import (
    ChatService,
)
from fastapi import Depends

from database.models.user import User
from services.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.post("")
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):

    service = ChatService()

    result = await service.ask(
        conversation_id=request.conversation_id,
        document_id=request.document_id,
        question=request.question,
    )
    return {
        "success": True,
        "data": result,
    }