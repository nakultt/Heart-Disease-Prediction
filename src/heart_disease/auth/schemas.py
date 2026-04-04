"""Pydantic models for auth request/response bodies."""

from typing import Literal

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """Body for POST /auth/register — persisted in MongoDB."""

    username: str = Field(..., min_length=3, max_length=128)
    password: str = Field(..., min_length=6, max_length=128)
    age: int = Field(..., ge=1, le=120)
    gender: Literal["male", "female", "other"]
    weight_kg: float = Field(..., gt=0, le=500)
    height_cm: float = Field(..., gt=0, le=300)


class UserLogin(BaseModel):
    """Body for POST /auth/login."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Standard OAuth2-style token payload."""

    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    """Returned after registration (no password)."""

    username: str
    age: int
    gender: str
    weight_kg: float
    height_cm: float
    smoking: str
    stress: str
    message: str = "Registration successful. You can log in now."
