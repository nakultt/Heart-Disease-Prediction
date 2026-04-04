"""
FastAPI dependencies: extract the current user from a Bearer JWT.

Used to protect routes—only requests with a valid token can proceed.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from src.heart_disease.auth import jwt_handler
from src.heart_disease.auth import users_store

# Tells FastAPI to read Authorization: Bearer <token>
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    """
    Validate the JWT and return the username (subject).

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

    user = users_store.get_user(username)
    if user is None:
        raise credentials_exception

    return user["username"]
