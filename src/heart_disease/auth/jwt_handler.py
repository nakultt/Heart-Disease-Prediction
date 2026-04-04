"""
Create and validate JWT access tokens using python-jose.

The 'sub' (subject) claim stores the username. 'exp' is required for expiry.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from src.heart_disease.core.config import get_settings


def create_access_token(subject_username: str, expires_minutes: int | None = None) -> str:
    """
    Build a signed JWT string.

    Args:
        subject_username: Username to embed in the token (claim 'sub').
        expires_minutes: Override default lifetime from settings.
    """
    settings = get_settings()
    expire_delta = timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    expire = datetime.now(timezone.utc) + expire_delta
    to_encode = {"sub": subject_username, "exp": expire}
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT. Raises jose.JWTError if invalid or expired.

    Returns the payload dict (includes 'sub' and 'exp').
    """
    settings = get_settings()
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
