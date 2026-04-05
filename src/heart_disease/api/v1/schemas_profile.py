"""Profile and history API models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class UserProfileResponse(BaseModel):
    username: str
    age: int
    gender: str
    weight_kg: float = Field(..., description="Weight in kilograms")
    height_cm: float = Field(..., description="Height in centimeters")
    smoking: str
    stress: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserProfileUpdate(BaseModel):
    """Partial update — only send fields to change."""

    age: int | None = Field(None, ge=1, le=120)
    gender: Literal["male", "female", "other"] | None = None
    weight_kg: float | None = Field(None, gt=0, le=500)
    height_cm: float | None = Field(None, gt=0, le=300)
    smoking: Literal["never", "former", "current"] | None = None
    stress: Literal["low", "moderate", "high"] | None = None


class PredictionHistoryItem(BaseModel):
    id: str
    created_at: datetime | None
    prediction: int
    probability: float
    risk_level: str
    clinical_input: dict | None = None
