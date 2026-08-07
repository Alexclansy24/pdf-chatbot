from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from database.models.user import User

from services.auth.utils import decode_access_token
from services.users.repository import UserRepository

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

def get_user_repository() -> UserRepository:
    return UserRepository()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = credentials.credentials
    user_id = decode_access_token(token)
    repository = UserRepository()
    user = await repository.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

    return user