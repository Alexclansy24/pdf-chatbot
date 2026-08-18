import pytest

from services.embeddings.service import EmbeddingService


@pytest.mark.asyncio
async def test_embedding_generation():

    service = EmbeddingService()

    vector = await service.embed_text(
        "This is a test document."
    )

    assert vector is not None

    assert len(vector) == 3072