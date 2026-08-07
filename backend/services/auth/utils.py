from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from core.config import settings
# Configure password hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )

def create_access_token(
    user_id: UUID,
) -> str:
    """
    Generate a JWT access token for a user.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> UUID:
    """
    Decode a JWT and return the user ID.
    Raises JWTError if the token is invalid.
    """

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )

    user_id = payload.get("sub")

    if user_id is None:
        raise JWTError("Missing subject claim")

    return UUID(user_id)   