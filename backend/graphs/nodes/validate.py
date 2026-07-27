from graphs.states.rag_state import (
    RAGState,
)


def validate_node(
    state: RAGState,
):

    context = state["context"]

    if not context.strip():

        return {
            "context": "",
            "retrieved_chunks": 0,
        }

    return {}