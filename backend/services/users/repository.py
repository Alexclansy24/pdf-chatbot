from uuid import UUID

from sqlalchemy import select

from database.models.user import User
from database.session import AsyncSessionLocal


class UserRepository:

    async def create_user(
        self,
        *,
        email: str,
        name: str,
        hashed_password: str,
    ) -> User:

        async with AsyncSessionLocal() as session:

            user = User(
                email=email,
                name=name,
                hashed_password=hashed_password,
            )

            session.add(user)

            await session.commit()

            await session.refresh(user)

            return user

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(User).where(
                    User.email == email
                )
            )

            return result.scalar_one_or_none()

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        async with AsyncSessionLocal() as session:

            result = await session.execute(
                select(User).where(
                    User.id == user_id
                )
            )

            return result.scalar_one_or_none()