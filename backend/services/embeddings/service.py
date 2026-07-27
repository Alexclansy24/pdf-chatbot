from services.embeddings.client import (
    client,
)


class EmbeddingService:

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:

        response = (
            client.models.embed_content(
                model="models/gemini-embedding-001",
                contents=text,
            )
        )

        return response.embeddings[0].values