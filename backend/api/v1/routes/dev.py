from fastapi import APIRouter

from database.models.user import User
from database.session import AsyncSessionLocal

router = APIRouter(
    prefix="/dev",
    tags=["Dev"],
)


@router.post("/seed-user")
async def seed_user():

    async with AsyncSessionLocal() as db:

        user = User(
            id="11111111-1111-1111-1111-111111111111",
            email="dev@example.com",
            name="Developer",
            hashed_password="[PASSWORD]",
        )

        db.add(user)

        await db.commit()

    return {
        "success": True,
        "message": "User seeded",
        "data": {},
    }