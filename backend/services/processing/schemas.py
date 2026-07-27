from pydantic import BaseModel


class ParsedDocument(BaseModel):
    text: str
    page_count: int


class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    content: str
    chunk_index: int
  