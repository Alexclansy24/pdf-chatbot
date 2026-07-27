from services.embeddings.service import (
    EmbeddingService,
)
from vectorstore.repository import (
    VectorRepository,
)


class IndexingService:

    def __init__(self):

        self.embeddings = (
            EmbeddingService()
        )

        self.repository = (
            VectorRepository()
        )

    async def index_chunk(
        self,
        chunk,
    ):

        vector = (
            await self.embeddings.embed_text(
                chunk.content
            )
        )

        self.repository.upsert(
            vector=vector,
            payload={
                "document_id":
                    chunk.document_id,

                "chunk_id":
                    chunk.chunk_id,

                "chunk_index":
                    chunk.chunk_index,

                "content":
                    chunk.content,
            },
        )

    async def index_chunks(
        self,
        chunks,
    ):

        for chunk in chunks:

            await self.index_chunk(
                chunk
            )