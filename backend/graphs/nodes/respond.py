from graphs.states.rag_state import (
    RAGState,
)


def response_node(
    state: RAGState,
):

    return {
        "answer":
            state["answer"],

        "sources":
            state["sources"],
    }