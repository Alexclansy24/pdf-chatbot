from langchain_google_genai import (
    ChatGoogleGenerativeAI,
)

from core.config import settings

from graphs.states.rag_state import (
    RAGState,
)


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.1,
)


async def generate_node(
    state: RAGState,
):

    if state["retrieved_chunks"] == 0:

        return {
            "answer":
                (
                    "I could not find "
                    "relevant information "
                    "in the uploaded documents."
                )
        }

    prompt = f"""
Answer only from the provided context.

Context:
{state['context']}

Question:
{state['question']}
"""

    response = await llm.ainvoke(
        prompt
    )

    return {
        "answer":
            response.content
    }