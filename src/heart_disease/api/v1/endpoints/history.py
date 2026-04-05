"""Prediction history for the authenticated user."""

from fastapi import APIRouter, Depends

from src.heart_disease.api.v1.schemas_profile import PredictionHistoryItem
from src.heart_disease.auth.dependencies import get_current_user
from src.heart_disease.db import predictions_repo

router = APIRouter()


@router.get("/predictions/history", response_model=list[PredictionHistoryItem])
def list_prediction_history(
    current_user: str = Depends(get_current_user),
) -> list[PredictionHistoryItem]:
    rows = predictions_repo.list_for_user(current_user)
    return [PredictionHistoryItem(**row) for row in rows]
