from graphs.rag_graph import (
    rag_graph,
)


class GraphService:

    async def ask(
        self,
        question: str,
        conversation_id: str | None = None,
    ):

        result = await rag_graph.ainvoke(
            {
                "question":
                    question,
                "context":
                    "",
                "answer":
                    "",
                "retrieved_chunks":
                    0,
                "sources":
                    [],
            }
        )

        return result

    async def stream_answer(
    self,
    question: str,
    conversation_id: str | None = None,
    ):
        state = {
            "question": question,
            "context": "",
            "answer": "",
            "retrieved_chunks": 0,
            "sources": [],
            "conversation_id": conversation_id,
            "chat_history": "",
        }

        async for event in rag_graph.astream(
            state
        ):
            yield event