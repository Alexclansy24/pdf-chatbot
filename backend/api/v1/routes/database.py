from fastapi import APIRouter
from sqlalchemy import text

from database.session import AsyncSessionLocal

router = APIRouter(
    prefix="/database",
    tags=["Database"],
)


@router.get("/health")
async def database_health():
    async with AsyncSessionLocal() as session:
        await session.execute(text("SELECT 1"))

    return {
        "success": True,
        "message": "Database connection successful",
        "data": {},
    }