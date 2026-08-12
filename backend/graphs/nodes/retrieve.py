from graphs.states.rag_state import (
    RAGState,
)

from services.retrieval.service import (
    RetrievalService,
)


retriever = RetrievalService()


async def retrieve_node(
    state: RAGState,
):

    results = await retriever.retrieve(
        query=state["question"],
        limit=5,
        document_id=state.get("document_id"),
    )

    contexts = []
    sources = []

    for point in results.points:

        payload = point.payload

        contexts.append(
            payload.get(
                "content",
                ""
            )
        )

        sources.append(
            {
                "document_id":
                    payload.get(
                        "document_id"
                    ),

                "chunk_id":
                    payload.get(
                        "chunk_id"
                    ),

                "chunk_index":
                    payload.get(
                        "chunk_index"
                    ),

                "score":
                    point.score,
            }
        )
    
    return {
        "context": "\n\n".join(contexts),
        "retrieved_chunks": len(sources),
        "sources": sources,
    }