from pydantic import BaseModel, ConfigDict, EmailStr
from uuid import UUID

class RegisterRequest(BaseModel):
    email: EmailStr
    name: str
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str

    model_config = ConfigDict(
        from_attributes=True,
    )