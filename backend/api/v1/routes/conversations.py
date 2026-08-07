from fastapi import HTTPException
from services.auth.dependencies import get_current_user
from fastapi import Depends
from database.models.user import User
from uuid import UUID

from fastapi import APIRouter

from services.conversations.repository import (
    ConversationRepository,
)
from schemas.conversation import (
    CreateConversationRequest,
)
router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: UUID,
):

    repository = (
        ConversationRepository()
    )

    current_user: User = Depends(get_current_user)
    conversation = (
        await repository.get(
            conversation_id=conversation_id,
            user_id=current_user.id,
        )
    )
    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return {
        "success": True,
        "data": (
            None
            if conversation is None
            else {
                "id": str(
                    conversation.id
                ),
                "title":
                    conversation.title,
            }
        ),
    }

@router.post("/test")
async def create_test_conversation():

    repository = ConversationRepository()

    conversation = await repository.create(
        user_id= UUID("11111111-1111-1111-1111-111111111111"),
        title="Test Conversation",
    )

    return {
        "success": True,
        "data": {
            "id": str(conversation.id),
            "title": conversation.title,
        },
    }

@router.post("")
async def create_conversation(
    request: CreateConversationRequest,
):
    repository = (
        ConversationRepository()
    )

    # Temporary user id
    current_user: User = Depends(get_current_user)

    conversation = (
        await repository.create(
            user_id=current_user.id,
            title=request.title,
        )
    )

    return {
        "success": True,
        "data": {
            "id": str(
                conversation.id
            ),
            "title":
                conversation.title,
        },
    }

@router.get("")
async def list_conversations():
    current_user: User = Depends(get_current_user)
    repository = (
        ConversationRepository()
    )

    user_id = current_user.id

    conversations = (
        await repository.list_by_user(
            user_id
        )
    )

    return {
        "success": True,
        "data": [
            {
                "id": str(c.id),
                "title": c.title,
            }
            for c in conversations
        ],
    }