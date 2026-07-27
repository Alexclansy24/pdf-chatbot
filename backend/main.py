from fastapi import FastAPI

from api.v1.router import api_router
from core.config import settings
from core.logging import configure_logging
from vectorstore.collections import (
    CollectionManager,
)

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
)

app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


@app.get("/")
async def root():
    return {
        "success": True,
        "message": "PDF Chatbot API",
        "data": {},
    }

@app.on_event("startup")
async def startup():

    CollectionManager.create_collection()
