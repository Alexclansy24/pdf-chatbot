from uuid import UUID

from fastapi import APIRouter

from services.conversations.repository import (
    ConversationRepository,
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