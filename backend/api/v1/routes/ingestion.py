from services.auth.dependencies import get_current_user
from database.models.user import User
from fastapi import Depends
from storage.local import LocalStorageProvider
from core.config import settings
from pathlib import Path
from uuid import UUID

from fastapi import APIRouter, UploadFile

from services.ingestion.service import IngestionService
from database.models.enums import DocumentStatus
from services.documents.repository import DocumentRepository  # adjust import path

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)



@router.post("/pdf")
async def upload_pdf(file: UploadFile, current_user: User = Depends(get_current_user)):

    storage = LocalStorageProvider(settings.UPLOAD_DIR)

    storage_path = await storage.upload(
        file_bytes=await file.read(),
        path=file.filename,
    )

    document_repository = DocumentRepository()

    # 1. Create the Postgres row first — generates the real document.id
    #    status defaults to UPLOADED via the model, but set explicitly for clarity
    document = await document_repository.create(
        filename=file.filename,
        storage_path=storage_path,
        user_id=current_user.id,
    )

    # 2. Mark as actively processing
    await document_repository.update(
        document_id=str(document.id),
        status=DocumentStatus.PROCESSING,
    )

    service = IngestionService()

    try:
        # 3. Pass the real Postgres ID into process_pdf — no more uuid4()
        result = await service.process_pdf(
            file_path=storage_path,
            document_id=str(document.id),
        )

        # 4. Update with final counts + status
        await document_repository.update(
            document_id=str(document.id),
            page_count=result["pages"],
            chunk_count=result["chunks"],
            status=DocumentStatus.INDEXED,
        )

    except Exception:
        await document_repository.update(
            document_id=str(document.id),
            status=DocumentStatus.FAILED,
        )
        raise

    return {
        "success": True,
        "data": {
            "document_id": str(document.id),
            **result,
        },
    }