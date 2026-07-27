from uuid import uuid4

from services.processing.schemas import Chunk


class DocumentChunker:

    def chunk(
        self,
        text: str,
        document_id: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ) -> list[Chunk]:

        if overlap >= chunk_size:
            raise ValueError(
                "overlap must be smaller than chunk_size"
            )

        step = chunk_size - overlap

        chunks: list[Chunk] = []

        start = 0
        index = 0

        while start < len(text):

            end = start + chunk_size

            content = text[start:end]

            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    document_id=document_id,
                    content=content,
                    chunk_index=index,
                )
            )

            start += step
            index += 1

        return chunks