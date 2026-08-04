from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50
    )

    budget: float | None = Field(
        default=None,
        ge=0
    )

    color: str | None = Field(
        default=None,
        max_length=50
    )


class CategoryResponse(BaseModel):
    id: int
    name: str
    budget: float | None = None
    total_spent: float = 0
    is_over_budget: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    budget: float | None = Field(
        default=None,
        ge=0
    )

    color: str | None = Field(
        default=None,
        max_length=50
    )