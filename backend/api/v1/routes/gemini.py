from fastapi import APIRouter
from google import genai

from core.config import settings

router = APIRouter(
    prefix="/gemini",
    tags=["Gemini"],
)


@router.get("/models")
async def list_models():
    client = genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )

    models = []

    for model in client.models.list():
        models.append(model.name)

    return {
        "success": True,
        "data": models,
    }

@router.get("/embedding-models")
async def embedding_models():
    client = genai.Client(
        api_key=settings.GOOGLE_API_KEY
    )

    models = []

    for model in client.models.list():
        if "embed" in model.name.lower():
            models.append(model.name)

    return {
        "success": True,
        "data": models,
    }    