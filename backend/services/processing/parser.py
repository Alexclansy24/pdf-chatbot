import fitz

from services.processing.schemas import (
    ParsedDocument,
)


class PDFParser:

    def parse(
        self,
        file_path: str,
    ) -> ParsedDocument:

        doc = fitz.open(file_path)

        text_parts = []

        for page in doc:
            text_parts.append(
                page.get_text()
            )

        return ParsedDocument(
            text="\n".join(text_parts),
            page_count=len(doc),
        )