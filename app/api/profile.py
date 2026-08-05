from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.services.profile_services import get_profile_service,update_profile_service
from app.schemas.common_response_schema import ApiResponse

from app.schemas.profile import (
    ProfileResponse,
    ProfileUpdate
)


router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)

@router.get("/", response_model=ApiResponse[ProfileResponse])

async def get_profile(
    current_user: User = Depends(get_current_user)
):
    result = get_profile_service(current_user)

    return ApiResponse(
        message="Profile fetched successfully",
        data=result
    )

@router.patch("/", response_model=ApiResponse[ProfileResponse])

async def update_profile(
    profile_data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)

):

    result = await update_profile_service(
        db,
        profile_data,
        current_user
    )

    return ApiResponse(
        message="Profile updated successfully",
        data=result

    )

@router.get("/test-error")
async def test_error():
        raise ValueError(
            "SECRET INTERNAL DATABASE INFORMATION"
        )