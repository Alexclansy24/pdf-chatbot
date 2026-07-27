from services.retrieval.constants import MIN_RELEVANCE_SCORE
from fastapi import APIRouter

from services.retrieval.service import (
    RetrievalService,
)
from pydantic import BaseModel


class SearchRequest(BaseModel):
    query: str
    limit: int = 5
    document_id: str | None = None

router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.get("/test")
async def retrieval_test():

    service = RetrievalService()

    results = await service.retrieve(
        "What is LangGraph?"
    )

    payloads = []

    for point in results.points:

        payloads.append(
            {
                "score": point.score,
                "content": point.payload.get(
                    "content"
                ),
            }
        )

    return {
        "success": True,
        "data": payloads,
    }

@router.post("/search")
async def search(
    request: SearchRequest,
):

    service = RetrievalService()

    results = await service.retrieve(
        query=request.query,
        limit=request.limit,
    )


    payloads = []

    for point in results.points:

        if point.score < MIN_RELEVANCE_SCORE:
            continue

        payloads.append(
            {
                "score": point.score,
                "content": point.payload.get(
                    "content"
                ),
                "document_id":
                    point.payload.get(
                        "document_id"
                    ),
            }
        )

    return {
        "success": True,
        "data": payloads,
    }