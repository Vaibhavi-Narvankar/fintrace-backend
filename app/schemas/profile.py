from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ProfileResponse(BaseModel):
    id: int
    email: str
    name: str | None = None
    profile_picture: str | None = None
    currency: str
    timezone: str
    monthly_income: Decimal | None = None
    monthly_salary_date: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    profile_picture: str | None = Field(
        default=None,
        max_length=500
    )

    currency: str | None = Field(
        default=None,
        min_length=3,
        max_length=3
    )

    timezone: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    monthly_income: Decimal | None = Field(
        default=None,
        ge=0
    )

    monthly_salary_date: int | None = Field(
        default=None,
        ge=1,
        le=31
    )