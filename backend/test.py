import asyncio

from services.auth.schemas import LoginRequest
from services.auth.service import AuthService
from services.users.repository import UserRepository


async def main():
    service = AuthService(
        repository=UserRepository(),
    )

    token = await service.login(
        LoginRequest(
            email="alex123@example.com",
            password="hello123",
        )
    )

    print(token)


asyncio.run(main())