from uuid import uuid4

from qdrant_client.models import (
    Filter, PointStruct, FieldCondition, MatchValue,
)

from core.config import settings
from vectorstore.client import qdrant_client


class VectorRepository:

    def search(
        self,
        vector: list[float],
        limit: int = 5,
        document_id: str | None = None,
    ):
        query_filter = None

        if document_id:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=str(document_id))
                    )
                ]
            )

        return qdrant_client.query_points(
            collection_name=settings.QDRANT_COLLECTION,
            query=vector,
            limit=limit,
            query_filter=query_filter,
        )

    def upsert(
        self,
        vector: list[float],
        payload: dict,
    ):
        point = PointStruct(
            id=str(uuid4()),
            vector=vector,
            payload=payload,
        )

        qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=[point],
        )

    def delete_by_document_id(self, document_id: str):
        qdrant_client.delete(
            collection_name=settings.QDRANT_COLLECTION,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=str(document_id))
                    )
                ]
            ),
        )