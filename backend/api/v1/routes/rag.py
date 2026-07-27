from fastapi import APIRouter

from schemas.rag import RAGRequest
from services.rag.service import RAGService
from services.graph.service import (
    GraphService,
)

router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


@router.post("/ask")
async def ask(
    request: RAGRequest,
):

    service = RAGService()

    result = await service.answer(
        request.question
    )

    return {
        "success": True,
        "data": result,
    }



@router.post("/graph")
async def graph_test(
    request: RAGRequest,
):

    service = GraphService()

    result = await service.ask(
        request.question
    )

    return {
        "success": True,
        "data": result,
    }