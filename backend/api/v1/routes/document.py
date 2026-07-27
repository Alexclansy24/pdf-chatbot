from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile

from database.dependencies import get_db
from repositories.document import DocumentRepository
from services.document_service import DocumentService
from storage.factory import get_storage
from utils.dev_user import DEV_USER_ID

router = APIRouter(
    prefix="/document",
    tags=["Documents"],
)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db=Depends(get_db),
):

    repository = DocumentRepository(db)

    service = DocumentService(
        repository=repository,
        storage=get_storage(),
    )

    document = await service.upload_document(
        user_id=DEV_USER_ID,
        file=file,
    )

    return {
        "success": True,
        "message": "Document uploaded",
        "data": {
            "id": str(document.id),
            "filename": document.filename,
            "status": document.status,
        },
    }