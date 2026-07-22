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