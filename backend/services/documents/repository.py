from uuid import UUID

from sqlalchemy import select

from database.session import AsyncSessionLocal
from database.models.document import Document


class DocumentRepository:

    async def create(
        self,
        filename: str,
        storage_path: str,
        user_id: UUID,
    ):
        async with AsyncSessionLocal() as session:

            document = Document(
                filename=filename,
                storage_path=storage_path,
                user_id=user_id,
                page_count=0,
                chunk_count=0,
            )

            session.add(document)
            await session.commit()
            await session.refresh(document)

            return document

    async def list_documents(
        self,
        user_id: str,
    ):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Document)
                .where(Document.user_id == user_id)
                .order_by(Document.created_at.desc())
            )
            return result.scalars().all()

    async def get_by_id(self, document_id: str,user_id: str,):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Document).where(
                    Document.id == document_id,
                    Document.user_id == user_id,
                )
            )
            return result.scalar_one_or_none()


    async def update(self, document_id: str, **fields):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Document).where(Document.id == document_id)
            )
            document = result.scalar_one_or_none()

            if document is None:
                raise ValueError(f"Document {document_id} not found")

            for key, value in fields.items():
                setattr(document, key, value)

            await session.commit()
            await session.refresh(document)

            return document

    async def delete(self, document_id: str):
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Document).where(Document.id == document_id)
            )
            document = result.scalar_one_or_none()

            if document is None:
                return None

            await session.delete(document)
            await session.commit()

            return document