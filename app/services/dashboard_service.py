from decimal import Decimal
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.dashboard import (
    DashboardTrendResponse,
    TrendPoint,
)
from datetime import datetime

def get_dashboard_summary_service(
    db: Session,
    current_user: User
) -> DashboardSummaryResponse:
   total_expense = (
       db.query(
           func.coalesce(
               func.sum(Expense.expense_amount),
               0
           )
       )
       .filter(
           Expense.user_id == current_user.id,
           Expense.is_deleted == False
       )
       .scalar()
   )
   total_categories = (
       db.query(
           func.count(Category.id)
       )
       .filter(
           Category.user_id == current_user.id,
           Category.is_deleted == False
       )
       .scalar()
   )
   monthly_income = current_user.monthly_income
   remaining_balance = (
       monthly_income - total_expense
       if monthly_income is not None
       else Decimal("0")
   )
   return DashboardSummaryResponse(
       total_expense=total_expense,
       total_categories=total_categories,
       monthly_income=monthly_income,
       remaining_balance=remaining_balance
   )

def get_dashboard_trends_service(
    db: Session,
    current_user: User,
    period: str
):
    current_year = datetime.now().year

    results = (
        db.query(
            func.date_trunc(
                "month",
                Expense.expense_date
            ).label("month"),
            func.coalesce(
                func.sum(Expense.expense_amount),
                0
            ).label("amount")
        )
        .filter(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            extract(
                "year",
                Expense.expense_date
            ) == current_year
        )
        .group_by("month")
        .order_by("month")
        .all()
    )

    trends = [
        TrendPoint(
            label=row.month.strftime("%b"),
            amount=row.amount
        )
        for row in results
    ]

    return DashboardTrendResponse(trends=trends)