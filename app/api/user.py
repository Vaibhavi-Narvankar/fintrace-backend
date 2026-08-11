from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse,RefreshTokenRequest
from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_services import (user_login_service, create_user_service, get_user_service,refresh_access_token_service)
from app.schemas.common_response_schema import ApiResponse


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/", response_model=ApiResponse[UserResponse])
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await create_user_service(db, user)
    return ApiResponse(
        message="User created successfully",
        data=result
    )

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    return await user_login_service(db, form_data)

@router.get("/", response_model=ApiResponse[list[UserResponse]])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_user_service(db, current_user)
    return ApiResponse(
        message="Users fetched successfully",
        data=result
    )

@router.post("/refresh")
async def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await refresh_access_token_service(
        db,
        token_data.refresh_token
    )
    return ApiResponse(
        message="Access token refreshed successfully",
        data=result
    )