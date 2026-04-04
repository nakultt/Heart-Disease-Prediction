"""
FastAPI dependencies: extract the current user from a Bearer JWT.

User must still exist in MongoDB.
"""

from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from src.heart_disease.auth import jwt_handler
from src.heart_disease.db import users_repo

security = HTTPBearer()


def get_current_user_record(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict[str, Any]:
    """
    Validate the JWT and return the user document from MongoDB.

    Raises 401 if the token is missing, invalid, or the user no longer exists.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_handler.decode_access_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_repo.find_user_by_username(username)
    if user is None:
        raise credentials_exception

    return user


def get_current_user(
    user: dict[str, Any] = Depends(get_current_user_record),
) -> str:
    """Username for endpoints that only need the subject string (single DB lookup per request)."""
    return str(user["username"])
