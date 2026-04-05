"""Current user profile (read + update)."""

from fastapi import APIRouter, Depends, HTTPException, status

from src.heart_disease.api.v1.schemas_profile import UserProfileResponse, UserProfileUpdate
from src.heart_disease.auth.dependencies import get_current_user, get_current_user_record
from src.heart_disease.db import users_repo

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
def read_my_profile(user: dict = Depends(get_current_user_record)) -> UserProfileResponse:
    return UserProfileResponse(**users_repo.profile_public(user))


@router.patch("/profile", response_model=UserProfileResponse)
def update_my_profile(
    body: UserProfileUpdate,
    current_user: str = Depends(get_current_user),
) -> UserProfileResponse:
    data = body.model_dump(exclude_unset=True)
    updated = users_repo.update_user_profile(current_user, data)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserProfileResponse(**updated)
