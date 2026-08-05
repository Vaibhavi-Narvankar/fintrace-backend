from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, EmailStr, Field,field_validator


class UserCreate(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=8,
        max_length=128
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    monthly_income: Decimal | None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=128
    )


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        min_length=1
    )