from services.processing.chunker import DocumentChunker


def test_chunker_creates_chunks():

    chunker = DocumentChunker()

    text = """
    LangGraph is used to build stateful
    applications with language models.
    """

    chunks = chunker.chunk(
        text=text,
        document_id="test-document-id",
    )

    assert len(chunks) > 0

    assert chunks[0].document_id == "test-document-id"

    assert chunks[0].content