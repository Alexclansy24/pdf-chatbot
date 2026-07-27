from uuid import uuid4
import asyncio
from anyio._core import _eventloop
from services.processing.chunker import (
    DocumentChunker,
)
from services.processing.parser import (
    PDFParser,
)


class DocumentProcessor:

    def __init__(self):
        self.parser = PDFParser()
        self.chunker = DocumentChunker()

    async def process(
        self,
        file_path: str,
        document_id: str,
    ):

        loop = asyncio.get_running_loop()

        parsed = await loop.run_in_executor(
            None,
            self.parser.parse,
            file_path,
        )

        chunks = await loop.run_in_executor(
            None,
            self.chunker.chunk,
            parsed.text,
            document_id,
        )

        return {
            "document_id": document_id,
            "pages": parsed.page_count,
            "text_length": len(parsed.text),
            "chunks": chunks,
        }