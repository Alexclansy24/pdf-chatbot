from qdrant_client.models import (
    Distance,
    VectorParams,
)

from core.config import settings
from vectorstore.client import (
    qdrant_client,
)
from core.constants import (
    EMBEDDING_DIMENSION,
)


class CollectionManager:

    @staticmethod
    def create_collection():

        collections = (
            qdrant_client.get_collections()
        )

        existing = [
            c.name
            for c in collections.collections
        ]

        if (
            settings.QDRANT_COLLECTION
            in existing
        ):
            return

        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE,
            ),
        )