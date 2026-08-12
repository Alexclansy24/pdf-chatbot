from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import settings
from graphs.states.rag_state import RAGState


llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    google_api_key=settings.GOOGLE_API_KEY,
    temperature=0.1,
)


async def generate_node(
    state: RAGState,
):

    # No relevant chunks found
    if state["retrieved_chunks"] == 0:

        return {
            "answer": (
                "I could not find that information "
                "in the uploaded document."
            )
        }

    prompt = f"""
You are a PDF question-answering assistant.

Your ONLY source of information is the PDF CONTEXT provided below.

STRICT RULES:

1. Answer ONLY using information contained in the PDF CONTEXT.
2. Do NOT use your general knowledge.
3. Do NOT use information from the internet.
4. Do NOT make assumptions.
5. Do NOT invent information.
6. If the answer is not present in the PDF CONTEXT, say:
   "I could not find that information in the uploaded document."
7. Keep the answer directly related to the user's question.
8. If the context contains conflicting information, mention the
   conflict instead of choosing an answer from outside knowledge.

PDF CONTEXT:
--------------------
{state["context"]}
--------------------

USER QUESTION:
{state["question"]}

ANSWER:
"""

    response = await llm.ainvoke(prompt)

    return {
        "answer": response.content
    }