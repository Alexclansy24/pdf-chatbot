from database.models.user import User
from services.auth.dependencies import get_current_user
from storage.local import LocalStorageProvider
from vectorstore.repository import VectorRepository
from services.documents.repository import DocumentRepository
from services.documents.service import DocumentService
from uuid import UUID
from core.config import settings
from fastapi import APIRouter, HTTPException, Depends



router = APIRouter(prefix="/documents", tags=["Documents"])


def get_document_service() -> DocumentService:
    return DocumentService(
        repository=DocumentRepository(),
        vector_repository=VectorRepository(),
        storage=LocalStorageProvider(
            upload_dir=settings.UPLOAD_DIR,
        ),
    )

@router.get("")
async def list_documents(
    current_user: User = Depends(get_current_user),
):
    service = get_document_service()
    documents = await service.list_documents(
        user_id=str(current_user.id),
    )

    return [
        {
            "id": str(doc.id),
            "filename": doc.filename,
            "status": doc.status,
            "page_count": doc.page_count,
            "chunk_count": doc.chunk_count,
        }
        for doc in documents
    ]


@router.get("/{document_id}")
async def get_document(document_id: UUID, 
    current_user: User = Depends(get_current_user)):
    service = get_document_service()

    try:
        document = await service.get_document(
            document_id=str(document_id),
            user_id=str(current_user.id),
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")

    return {
        "id": str(document.id),
        "filename": document.filename,
        "status": document.status,
        "page_count": document.page_count,
        "chunk_count": document.chunk_count,
    }

@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    current_user: User = Depends(get_current_user),
    service: DocumentService = Depends(get_document_service),
):
    try:
        await service.delete_document(
            document_id=str(document_id),
            user_id=str(current_user.id),
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Document not found")

    return {"success": True, "message": "Document deleted"}