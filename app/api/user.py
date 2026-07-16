from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse,RefreshTokenRequest
from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_services import (user_login_service, create_user_service, get_user_service,refresh_access_token_service)


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user)



@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    return user_login_service(db, form_data)

@router.get("/", response_model=list[UserResponse])
def get_users(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)  # 🔒 protected
):
    return get_user_service(db, current_user)

@router.post("/refresh")
def refresh_access_token(
    token_data: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    return refresh_access_token_service(
        db,
        token_data.refresh_token
    )

