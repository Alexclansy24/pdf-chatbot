from uuid import UUID

from fastapi import APIRouter

from services.messages.repository import (
    MessageRepository,
)

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.get(
    "/{conversation_id}"
)
async def get_messages(
    conversation_id: UUID,
):

    repository = (
        MessageRepository()
    )

    messages = (
        await repository.history(
            conversation_id
        )
    )

    return {
        "success": True,
        "data": [
            {
                "id": str(msg.id),
                "role": str(
                    msg.role
                ),
                "content":
                    msg.content,
            }
            for msg in messages
        ],
    }