from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from database.models.document import Document
from database.models.enums import DocumentStatus
from services.documents.repository import DocumentRepository
from storage.base import StorageProvider


class DocumentService:
    def __init__(
        self,
        repository: DocumentRepository,
        storage: StorageProvider,
    ):
        self.repository = repository
        self.storage = storage

    async def upload_document(
        self,
        user_id,
        file: UploadFile,
    ) -> Document:

        extension = Path(
            file.filename
        ).suffix.lower()

        if extension != ".pdf":
            raise ValueError(
                "Only PDF files allowed"
            )

        file_bytes = await file.read()


        document_id = uuid4()

        storage_path = (
            f"documents/{document_id}.pdf"
        )

        await self.storage.upload(
            file_bytes=file_bytes,
            path=storage_path,
        )

        document = Document(
            id=document_id,
            user_id=user_id,
            filename=file.filename,
            status=DocumentStatus.UPLOADED,
            storage_path=storage_path,
            page_count=0,
            chunk_count=0,
        )

        return await self.repository.create(
            document
        )