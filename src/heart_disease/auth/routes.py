"""
Auth HTTP routes: register a new user and log in to receive a JWT.
"""

from fastapi import APIRouter, HTTPException, status

from src.heart_disease.auth import password as pwd_utils
from src.heart_disease.auth import users_store
from src.heart_disease.auth.jwt_handler import create_access_token
from src.heart_disease.auth.schemas import TokenResponse, UserLogin, UserPublic, UserRegister

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(body: UserRegister) -> UserPublic:
    """
    Create a new account. Password is hashed before storage.
    """
    username = body.username.strip()
    password = body.password.strip()
    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters (after trimming spaces).",
        )
    if users_store.username_exists(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    hashed = pwd_utils.hash_password(password)
    users_store.add_user(username, hashed)
    return UserPublic(username=username)


@router.post("/login", response_model=TokenResponse)
def login_user(body: UserLogin) -> TokenResponse:
    """
    Check username/password and return a JWT access token.
    """
    username = body.username.strip()
    password = body.password.strip()
    if not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = users_store.get_user(username)
    if user is None or not pwd_utils.verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject_username=user["username"])
    return TokenResponse(access_token=access_token)
