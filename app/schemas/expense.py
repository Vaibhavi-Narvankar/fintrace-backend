from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, Field,field_validator


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

    @field_validator("expense_name")
    @classmethod
    def normalize_expense_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Expense name cannot be empty")

        return value

    @field_validator("payment_type")
    @classmethod
    def normalize_payment_type(cls, value: str) -> str:
        value = value.strip().upper()

        if not value:
            raise ValueError("Payment type cannot be empty")

        return value


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

    @field_validator("expense_name")
    @classmethod
    def normalize_expense_name(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip()

        if not value:
            raise ValueError("Expense name cannot be empty")

        return value


    @field_validator("payment_type")
    @classmethod
    def normalize_payment_type(cls, value: str | None) -> str | None:
        if value is None:
            return None

        value = value.strip().upper()

        if not value:
            raise ValueError("Payment type cannot be empty")

        return value