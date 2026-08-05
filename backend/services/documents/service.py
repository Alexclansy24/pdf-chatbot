from storage.base import StorageProvider
from vectorstore.repository import VectorRepository
from services.documents.repository import DocumentRepository
class DocumentService:

    def __init__(
        self,
        repository: DocumentRepository,
        vector_repository: VectorRepository,
        storage: StorageProvider,
    ):
        self.repository = repository
        self.vector_repository = vector_repository
        self.storage = storage

    async def list_documents(self):
        return await self.repository.list_documents()

    async def get_document(self, document_id: str):
        document = await self.repository.get_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {document_id} not found")
        return document

    async def delete_document(self, document_id: str):
        document = await self.repository.get_by_id(document_id)
        if document is None:
            raise ValueError(f"Document {document_id} not found")

        # 1. Delete Qdrant vectors
        self.vector_repository.delete_by_document_id(document_id)

        # 2. Delete uploaded file
        await self.storage.delete(document.storage_path)

        # 3. Delete Postgres row
        await self.repository.delete(document_id)

        return document