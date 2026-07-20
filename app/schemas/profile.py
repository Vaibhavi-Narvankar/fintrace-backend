from datetime import datetime
from pydantic import BaseModel


class ProfileResponse(BaseModel):
    id: int
    email: str
    name: str | None = None
    profile_picture: str | None = None
    currency: str
    timezone: str
    monthly_income: float | None = None
    monthly_salary_date: int | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    name: str | None = None
    profile_picture: str | None = None
    currency: str | None = None
    timezone: str | None = None
    monthly_income: float | None = None
    monthly_salary_date: int | None = None