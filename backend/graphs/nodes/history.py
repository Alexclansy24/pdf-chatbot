from uuid import UUID

from graphs.states.rag_state import (
    RAGState,
)

from services.messages.repository import (
    MessageRepository,
)


repository = MessageRepository()


async def history_node(
    state: RAGState,
):

    conversation_id = state.get(
        "conversation_id"
    )

    if not conversation_id:

        return {
            "chat_history": ""
        }

    messages = await repository.history(
        UUID(conversation_id)
    )

    history_lines = []

    for msg in messages:

        history_lines.append(
            f"{msg.role}: {msg.content}"
        )

    return {
        "chat_history":
            "\n".join(
                history_lines
            )
    }