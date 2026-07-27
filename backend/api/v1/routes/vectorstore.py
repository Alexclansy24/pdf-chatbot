from fastapi import APIRouter

from core.config import settings
from vectorstore.client import (
    qdrant_client
)

router = APIRouter(
    prefix="/vectorstore",
    tags=["Vector Store"],
)


@router.get("/health")
async def vector_health():

    collections = (
        qdrant_client.get_collections()
    )

    return {
        "success": True,
        "message": "Qdrant connected",
        "data": {
            "collections": [
                c.name
                for c in collections.collections
            ],
            "active": settings.QDRANT_COLLECTION,
        },
    }

@router.get("/collection")
async def collection_info():

    info = qdrant_client.get_collection(
        settings.QDRANT_COLLECTION
    )

    return {
        "success": True,
        "data": info.model_dump()
    }