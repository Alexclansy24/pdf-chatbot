from vectorstore.repository import VectorRepository


def test_vector_store_search():

    repository = VectorRepository()

    vector = [0.1] * 3072

    repository.upsert(
        vector=vector,
        payload={
            "document_id": "test-document",
            "chunk_id": "test-chunk",
            "chunk_index": 0,
            "content": "This is an integration test.",
        },
    )

    results = repository.search(
        vector=vector,
        limit=1,
    )

    assert results is not None
    assert len(results.points) > 0