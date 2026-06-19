from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.security import verify_password, create_access_token,hash_password
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User


def create_user_service(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)
    existing_user = db.query(User).filter(
        User.email == user.email,
        User.is_deleted == False
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    db_user = User(
        email=user.email,
        password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def user_login_service(
        db: Session,
        form_data: OAuth2PasswordRequestForm
):
    db_user = db.query(User).filter(User.email == form_data.username,User.is_deleted == False).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

def get_user_service(db: Session,current_user: User):
    users = db.query(User).filter(
    User.is_deleted == False
    ).all()
    return users