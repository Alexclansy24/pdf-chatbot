from sqlalchemy import select

from database.session import AsyncSessionLocal
from database.models.document import Document


class DocumentRepository:

    async def create(
        self,
        filename: str,
        storage_path: str,
    ):

        async with AsyncSessionLocal() as session:

            document = Document(
                filename=filename,
                storage_path=storage_path,
            )

            session.add(document)

            await session.commit()
            await session.refresh(document)

            return document

    async def list_documents(self):

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(Document)
            )

            return result.scalars().all()