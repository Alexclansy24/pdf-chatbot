from fastapi import requests
from fastapi import requests
from fastapi import requests
from services.auth.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)

from services.auth.utils import (
    hash_password,
    verify_password,
    create_access_token,
)

from services.users.repository import UserRepository

class AuthService:

    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    async def register(
        self,
        request: RegisterRequest,
    ):
        existing_user = await self.repository.get_by_email(
            request.email
        )

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = hash_password(
            request.password
        )

        user = await self.repository.create_user(
            email=request.email,
            name=request.name,
            hashed_password=hashed_password,
        )

        return user

    async def login(
        self,
        request: LoginRequest,
    ) -> TokenResponse:

        user = await self.repository.get_by_email(
            request.email
        )

        if user is None:
            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        token = create_access_token(
            user.id
        )

        return TokenResponse(
            access_token=token,
        )        