from fastapi import APIRouter

from services.embeddings.service import (
    EmbeddingService,
)

router = APIRouter(
    prefix="/embeddings",
    tags=["Embeddings"],
)


@router.get("/test")
async def embedding_test():

    service = EmbeddingService()

    vector = await service.embed_text(
        "Hello World"
    )

    return {
        "success": True,
        "data": {
            "dimension": len(vector),
            "sample": vector[:5]
        }
    }