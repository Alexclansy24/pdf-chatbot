from services.embeddings.service import (
    EmbeddingService,
)
from vectorstore.repository import (
    VectorRepository,
)


class RetrievalService:

    def __init__(self):

        self.embeddings = (
            EmbeddingService()
        )

        self.repository = (
            VectorRepository()
        )

    async def retrieve(
        self,
        query: str,
        limit: int = 5,
        document_id: str | None = None,
    ):

        query_vector = (
            await self.embeddings.embed_text(
                query
            )
        )

        results = self.repository.search(
            vector=query_vector,
            limit=limit,
            document_id=document_id,
        )
        return results