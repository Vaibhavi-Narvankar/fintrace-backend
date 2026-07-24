from decimal import Decimal
from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    total_expense: Decimal
    total_categories: int
    monthly_income: Decimal | None
    remaining_balance: Decimal

    model_config = {
        "from_attributes": True
    }

class TrendPoint(BaseModel):
    label: str
    amount: Decimal

class DashboardTrendResponse(BaseModel):
    trends: list[TrendPoint]


class HighestCategoryResponse(BaseModel):
    category_name: str
    category_color: str | None
    total_amount: Decimal

class BudgetProgressResponse(BaseModel):
    monthly_income: Decimal
    total_spent: Decimal
    remaining_balance: Decimal


class CategoryBreakdownItem(BaseModel):
    category_name: str
    category_color: str | None
    total_amount: Decimal


class CategoryBreakdownResponse(BaseModel):
    categories: list[CategoryBreakdownItem]


class RecurringExpenseItem(BaseModel):
    expense_name: str
    total_occurrences: int

class RecurringExpenseResponse(BaseModel):
    recurring_expenses: list[RecurringExpenseItem]