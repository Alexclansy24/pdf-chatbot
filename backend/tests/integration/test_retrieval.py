import pytest

from services.retrieval.service import RetrievalService


@pytest.mark.asyncio
async def test_retrieval():

    service = RetrievalService()

    results = await service.retrieve(
        query="What is this document about?",
        limit=5,
    )

    assert results is not None
    assert hasattr(results, "points")