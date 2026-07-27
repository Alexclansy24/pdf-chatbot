from graphs.rag_graph import (
    rag_graph,
)


class GraphService:

    async def ask(
        self,
        question: str,
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