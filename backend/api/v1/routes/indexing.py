from fastapi import APIRouter

from services.indexing.service import (
    IndexingService,
)
from services.processing.schemas import (
    Chunk,
)

router = APIRouter(
    prefix="/indexing",
    tags=["Indexing"],
)


@router.post("/test")
async def indexing_test():

    chunk = Chunk(
        chunk_id="test_chunk",
        document_id="test_document",
        chunk_index=0,
        content=(
            "LangGraph is a framework "
            "for building stateful AI agents."
        ),
    )

    service = IndexingService()

    await service.index_chunk(
        chunk
    )

    return {
        "success": True,
        "message": "Chunk indexed",
    }