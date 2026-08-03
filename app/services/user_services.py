from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from app.core.security import(
  verify_password, create_access_token,
  create_refresh_token ,hash_password,
  SECRET_KEY,ALGORITHM
  )
from app.schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User


async def create_user_service(
    db: AsyncSession,
    user: UserCreate
):
    hashed_password = hash_password(user.password)

    statement = select(User).where(
        User.email == user.email,
        User.is_deleted.is_(False)
    )

    result = await db.execute(statement)
    existing_user = result.scalars().first()

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

    await db.commit()
    await db.refresh(db_user)

    return db_user

async def user_login_service(
    db: AsyncSession,
    form_data: OAuth2PasswordRequestForm
):
    statement = select(User).where(
        User.email == form_data.username,
        User.is_deleted.is_(False)
    )

    result = await db.execute(statement)
    db_user = result.scalars().first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    access_token = create_access_token({
        "sub": db_user.email
    })

    refresh_token = create_refresh_token({
        "sub": db_user.email
    })

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

async def get_user_service(
    db: AsyncSession,
    current_user: User
):
    statement = select(User).where(
        User.is_deleted.is_(False)
    )

    result = await db.execute(statement)

    users = result.scalars().all()

    return users

async def refresh_access_token_service(
    db: AsyncSession,
    refresh_token: str
):
    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")
        token_type = payload.get("type")

        if email is None or token_type != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        statement = select(User).where(
            User.email == email,
            User.is_deleted.is_(False)
        )

        result = await db.execute(statement)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )

        new_access_token = create_access_token({
            "sub": user.email
        })

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )