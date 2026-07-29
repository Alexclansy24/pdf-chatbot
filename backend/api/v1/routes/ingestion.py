from fastapi import (
    APIRouter,
    UploadFile,
)

from services.ingestion.service import (
    IngestionService,
)

router = APIRouter(
    prefix="/ingestion",
    tags=["Ingestion"],
)
from pathlib import Path

UPLOAD_DIR = Path(
    "uploads"
)

UPLOAD_DIR.mkdir(
    exist_ok=True
)

@router.post("/pdf")
async def upload_pdf(
    file: UploadFile,
):

    file_path = (
        UPLOAD_DIR / file.filename
    )

    with open(
        file_path,
        "wb",
    ) as f:
        f.write(
            await file.read()
        )

    service = (
        IngestionService()
    )

    result = (
        await service.process_pdf(
            str(file_path)
        )
    )

    return {
        "success": True,
        "data": result,
    }