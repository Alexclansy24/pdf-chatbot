from fastapi import APIRouter

from storage.factory import get_storage

router = APIRouter(
    prefix="/storage",
    tags=["Storage"],
)


@router.get("/health")
async def storage_health():

    storage = get_storage()

    return {
        "success": True,
        "message": "Storage ready",
        "data": {
            "provider": storage.__class__.__name__
        }
    }