from langsmith._openapi_client.types import run_select_field
from services.processing.chunker import DocumentChunker
from services.processing.parser import PDFParser
from uuid import uuid4


from services.embeddings.service import EmbeddingService
from vectorstore.repository import VectorRepository


class IngestionService:

    def __init__(self):

        self.parser = PDFParser()

        self.chunker = DocumentChunker()

        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_repository = (
            VectorRepository()
        )

    async def process_pdf(
    self,
    file_path: str,
    ):

        document_id = str(uuid4())

        document = self.parser.parse(
            file_path
        )

        chunks = (
            self.chunker.chunk(
                text=document.text,
                document_id=document_id,
            )
        )

        for chunk in chunks:
            

            embedding = (
                await self.embedding_service
                .embed_text(
                    chunk.content
            )
        )

            self.vector_repository.upsert(
                vector=embedding,
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

        return {
            "document_id":
                document_id,
            "pages":
                document.page_count,
            "chunks":
                len(chunks),
        }