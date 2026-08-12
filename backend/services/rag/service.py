from langchain_google_genai import ChatGoogleGenerativeAI

from core.config import settings
from services.retrieval.service import RetrievalService


class RAGService:

    def __init__(self):
        self.retriever = RetrievalService()

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.1,
        )

    async def answer(
        self,
        question: str,
        document_id: str | None = None,
    ):
        # Retrieve only from the selected document
        results = await self.retriever.retrieve(
            query=question,
            limit=5,
            document_id=document_id,
        )

        contexts = []

        for point in results.points:
            content = point.payload.get("content", "")

            if content:
                contexts.append(content)

        context = "\n\n".join(contexts)

        prompt = f"""
You are a PDF question-answering assistant.

You MUST answer the question ONLY using the provided PDF context.

Do NOT use your general knowledge.
Do NOT use information from the internet.
Do NOT invent or assume information.

If the answer cannot be found in the provided context, respond exactly with:

"I could not find that information in the uploaded document."

PDF Context:
----------------
{context}
----------------

Question:
{question}

Answer:
"""

        response = await self.llm.ainvoke(prompt)

        return {
            "answer": response.content,
            "retrieved_chunks": len(contexts),
        }