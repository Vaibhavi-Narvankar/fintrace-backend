from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    expense_name: str = Field(
        min_length=1,
        max_length=100
    )

    expense_amount: Decimal = Field(
        gt=0
    )

    expense_date: date

    payment_type: str = Field(
        min_length=1,
        max_length=50
    )

    category_id: int = Field(
        gt=0
    )

    tax_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100
    )

    tax_amount: Decimal | None = Field(
        default=None,
        ge=0
    )


class ExpenseResponse(BaseModel):
    id: int
    expense_name: str
    expense_amount: Decimal
    expense_date: datetime
    payment_type: str

    tax_percent: Decimal | None = None
    tax_amount: Decimal | None = None

    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExpenseUpdate(BaseModel):
    expense_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    expense_amount: Decimal | None = Field(
        default=None,
        gt=0
    )

    expense_date: date | None = None

    payment_type: str | None = Field(
        default=None,
        min_length=1,
        max_length=50
    )

    category_id: int | None = Field(
        default=None,
        gt=0
    )

    tax_percent: Decimal | None = Field(
        default=None,
        ge=0,
        le=100
    )

    tax_amount: Decimal | None = Field(
        default=None,
        ge=0
    )