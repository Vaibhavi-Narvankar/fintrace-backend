from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse,RefreshTokenRequest
from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_services import (user_login_service, create_user_service, get_user_service,refresh_access_token_service)


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user_service(db, user)



@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    return await user_login_service(db, form_data)

@router.get("/", response_model=list[UserResponse])
async def get_users(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)  # 🔒 protected
):
    return await get_user_service(db, current_user)

@router.post("/refresh")
async def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    return await refresh_access_token_service(
        db,
        token_data.refresh_token
    )

