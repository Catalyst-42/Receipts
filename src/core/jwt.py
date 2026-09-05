from datetime import datetime, timedelta, timezone

from jose import jwt
from pydantic import UUID7

from src.config import settings


def create_access_token(
    subject: UUID7 | str,
    expires_days: int = settings.jwt_access_token_expire_days,
) -> str:
    """Returns access token for given user unique id"""
    expire = datetime.now(timezone.utc) + timedelta(days=expires_days)
    to_encode = {"sub": str(subject), "exp": expire}

    return jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_token(token: str) -> dict:
    """Decodes given access token"""
    return jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
