from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import settings
from services.retrieval.service import RetrievalService


class RAGService:

    def __init__(self):

        self.retriever = RetrievalService()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.1,
        )

    async def answer(
        self,
        question: str,
    ):

        results = await self.retriever.retrieve(
            query=question,
            limit=5,
        )

        contexts = []

        for point in results.points:

            contexts.append(
                point.payload.get(
                    "content",
                    "",
                )
            )

        context = "\n\n".join(contexts)

        prompt = f"""
You are a PDF assistant.

Answer ONLY using the provided context.

If the answer is not found in the context,
say:
"I could not find that information in the uploaded documents."

Context:
{context}

Question:
{question}
"""

        response = await self.llm.ainvoke(
            prompt
        )

        return {
            "answer": response.content,
            "sources": len(contexts),
        }