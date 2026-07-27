from sqlalchemy import select

from database.models.document import (
    Document,
)


class DocumentRepository:

    async def create(
        self,
        session,
        document: Document,
    ):

        session.add(document)

        await session.commit()

        await session.refresh(
            document
        )

        return document

    async def list(
        self,
        session,
    ):

        result = await session.execute(
            select(Document)
        )

        return result.scalars().all()