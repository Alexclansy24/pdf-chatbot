from qdrant_client import QdrantClient

from core.config import settings

qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
)