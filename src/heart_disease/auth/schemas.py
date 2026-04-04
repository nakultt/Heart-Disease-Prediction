"""Pydantic models for auth request/response bodies."""

from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    """Body for POST /auth/register."""

    username: str = Field(..., min_length=3, max_length=32, examples=["alice"])
    password: str = Field(..., min_length=6, max_length=128, examples=["secret123"])


class UserLogin(BaseModel):
    """Body for POST /auth/login."""

    username: str
    password: str


class TokenResponse(BaseModel):
    """Standard OAuth2-style token payload."""

    access_token: str
    token_type: str = "bearer"


class UserPublic(BaseModel):
    """Safe user info returned after registration (no password)."""

    username: str
    message: str = "Registration successful. You can log in now."
