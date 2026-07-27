from fastapi import APIRouter, Depends
from sqlalchemy import select

from database.models.document import (
    Document,
)
from database.dependencies import (
    get_db,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

@router.get("/")
async def list_documents(
    db=Depends(get_db),
):

    result = await db.execute(
        select(Document)
    )

    documents = (
        result.scalars().all()
    )

    return {
        "success": True,
        "data": documents,
    }