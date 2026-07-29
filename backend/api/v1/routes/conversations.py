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

    conversation = (
        await repository.get(
            conversation_id
        )
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
    user_id = UUID(
        "00000000-0000-0000-0000-000000000001"
    )

    conversation = (
        await repository.create(
            user_id=user_id,
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

    repository = (
        ConversationRepository()
    )

    user_id = UUID(
        "00000000-0000-0000-0000-000000000001"
    )

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