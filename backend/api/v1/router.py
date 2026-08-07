from fastapi import APIRouter

from api.v1.routes.health import router as health_router

from api.v1.routes.database import router as database_router

from api.v1.routes.storage import (
    router as storage_router
)  

from api.v1.routes.document import (
    router as document_router
)
from api.v1.routes.documents import (
    router as documents_router
)

from api.v1.routes.dev import (
    router as dev_router
)

from api.v1.routes.vectorstore import (
    router as vector_router
)
from api.v1.routes.gemini import (
    router as gemini_router
)
from api.v1.routes.embedding import (
    router as embedding_router
)
from api.v1.routes.indexing import (
    router as indexing_router
)
from api.v1.routes.retrieval import (
    router as retrieval_router
)
from api.v1.routes.rag import (
    router as rag_router
)
from api.v1.routes.conversations import (
    router as conversations_router,
)
from api.v1.routes.messages import (
    router as messages_router,
)
from api.v1.routes.chat import (
    router as chat_router,
)
from api.v1.routes.chat_stream import (
    router as chat_stream_router,
)
from api.v1.routes.ingestion import (
    router as ingestion_router
)
from api.v1.routes.auth import (
    router as auth_router
)

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(database_router)
api_router.include_router(storage_router)
api_router.include_router(document_router)
api_router.include_router(documents_router)
api_router.include_router(dev_router)
api_router.include_router(vector_router)
api_router.include_router(
    gemini_router
)
api_router.include_router(
    embedding_router
)
api_router.include_router(
    indexing_router
)
api_router.include_router(
    retrieval_router
)   
api_router.include_router(
    rag_router
)
api_router.include_router(
    conversations_router
)
api_router.include_router(
    messages_router
)
api_router.include_router(
    chat_router
)
api_router.include_router(
    chat_stream_router
)
api_router.include_router(
    ingestion_router
)
api_router.include_router(
    auth_router
)
