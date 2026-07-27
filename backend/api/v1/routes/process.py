from fastapi import APIRouter

from services.processing.processor import (
    DocumentProcessor,
)

router = APIRouter(
    prefix="/process",
    tags=["Processing"],
)


@router.post("/test")
async def test_process():

    processor = DocumentProcessor()

    result = await processor.process(
        "uploads/documents/YOUR_FILE.pdf"
    )

    return result