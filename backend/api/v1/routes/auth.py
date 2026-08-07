from fastapi import APIRouter, Depends, HTTPException
from database.models.user import User
from services.auth.dependencies import (
    get_current_user,
)
from services.auth.schemas import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from services.auth.service import AuthService
from services.users.repository import UserRepository

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_service() -> AuthService:
    return AuthService(
        repository=UserRepository(),
    )


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
)
async def register(
    request: RegisterRequest,
):
    service = get_auth_service()

    try:
        user = await service.register(request)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    return UserResponse.model_validate(user)


@router.post("/login")
async def login(
    request: LoginRequest,
    service: AuthService = Depends(get_auth_service),
):

    try:
        return await service.login(request)
    except ValueError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e),
        )

@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(get_current_user),
):
    return UserResponse.model_validate(
        current_user
    )