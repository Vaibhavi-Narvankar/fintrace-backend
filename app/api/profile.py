from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.profile_services import get_profile_service,update_profile_service

from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdate
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/", response_model=ProfileResponse)
def get_profile(
    current_user: User = Depends(get_current_user)
):

    return get_profile_service(current_user)

@router.patch("/", response_model=ProfileResponse)
def update_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return update_profile_service(
        db,
        profile_data,
        current_user
    )