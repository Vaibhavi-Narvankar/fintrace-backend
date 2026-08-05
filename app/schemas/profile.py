from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field,field_validator


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

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value


    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip().upper()


    @field_validator("timezone")
    @classmethod
    def normalize_timezone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip()

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        return value.strip().lower()


class ProfileUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    profile_picture: str | None = Field(default=None, max_length=500)
    currency: str | None = Field(default=None, min_length=3, max_length=3)
    timezone: str | None = Field(default=None, min_length=1, max_length=50)
    monthly_income: Decimal | None = Field(default=None, ge=0)
    monthly_salary_date: int | None = Field(default=None, ge=1, le=31)

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Name cannot be empty")

        return value

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, value: str | None) -> str | None:
        if value is None:
            return None

        return value.strip().upper()

    @field_validator("timezone")
    @classmethod
    def normalize_timezone(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Timezone cannot be empty")

        return value

    @field_validator("profile_picture")
    @classmethod
    def normalize_profile_picture(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        return value or None