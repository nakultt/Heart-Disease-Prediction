"""
Auth HTTP routes: register (MongoDB) and login (JWT).
"""

from fastapi import APIRouter, HTTPException, status

from src.heart_disease.auth import password as pwd_utils
from src.heart_disease.auth.jwt_handler import create_access_token
from src.heart_disease.auth.schemas import TokenResponse, UserLogin, UserPublic, UserRegister
from src.heart_disease.db import users_repo

router = APIRouter()


@router.post("/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def register_user(body: UserRegister) -> UserPublic:
    username = body.username.strip()
    password = body.password.strip()
    if len(password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters (after trimming spaces).",
        )
    if users_repo.username_taken(username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    hashed = pwd_utils.hash_password(password)
    users_repo.insert_user(
        username=username,
        password_hash=hashed,
        age=body.age,
        gender=body.gender,
        weight_kg=body.weight_kg,
        height_cm=body.height_cm,
        smoking="never",
        stress="low",
    )
    return UserPublic(
        username=username,
        age=body.age,
        gender=body.gender,
        weight_kg=body.weight_kg,
        height_cm=body.height_cm,
        smoking="never",
        stress="low",
    )


@router.post("/login", response_model=TokenResponse)
def login_user(body: UserLogin) -> TokenResponse:
    username = body.username.strip()
    password = body.password.strip()
    if not password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = users_repo.find_user_by_username(username)
    if user is None or not pwd_utils.verify_password(password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject_username=user["username"])
    return TokenResponse(access_token=access_token)
