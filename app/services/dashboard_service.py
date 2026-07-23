from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.expense import Expense
from app.models.category import Category
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.schemas.dashboard import (
    DashboardTrendResponse,
    TrendPoint,
    CategoryBreakdownItem,
    CategoryBreakdownResponse,
    HighestCategoryResponse,
    BudgetProgressResponse,
    RecurringExpenseItem,
    RecurringExpenseResponse,
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
    current_date = datetime.now()

    if period == "yearly":
        group_by_unit = "month"

        start_date = datetime(current_date.year, 1, 1)
        end_date = datetime(current_date.year + 1, 1, 1)

    elif period == "monthly":
        group_by_unit = "day"

        start_date = datetime(
            current_date.year,
            current_date.month,
            1
        )

        if current_date.month == 12:
            end_date = datetime(current_date.year + 1, 1, 1)
        else:
            end_date = datetime(
                current_date.year,
                current_date.month + 1,
                1
            )

    elif period == "weekly":
        group_by_unit = "day"

        start_date = current_date - timedelta(days=6)
        end_date = current_date + timedelta(days=1)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid period. Use weekly, monthly or yearly."
        )

    results = (
        db.query(
            func.date_trunc(
                group_by_unit,
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
             Expense.expense_date >= start_date,
             Expense.expense_date < end_date
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

def get_category_breakdown_service(
    db: Session,
    current_user: User,
):
    current_date = datetime.now()

    start_date = datetime(
        current_date.year,
        current_date.month,
        1
    )

    if current_date.month == 12:
        end_date = datetime(current_date.year + 1, 1, 1)
    else:
        end_date = datetime(
            current_date.year,
            current_date.month + 1,
            1
        )

    results = (
        db.query(
            Category.category_name.label("category_name"),
            Category.category_color.label("category_color"),
            func.coalesce(
                func.sum(Expense.expense_amount),
                0
            ).label("total_amount")
        )
        .join(
            Category,
            Expense.category_id == Category.id
        )
        .filter(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date,
        )
        .group_by(
            Category.id,
            Category.category_name,
            Category.category_color,
        )
        .order_by(
            func.sum(Expense.expense_amount).desc()
        )
        .all()
    )

    categories = [
        CategoryBreakdownItem(
            category_name=row.category_name,
            category_color=row.category_color,
            total_amount=row.total_amount,
        )
        for row in results
    ]

    return CategoryBreakdownResponse(
        categories=categories
    )

def get_highest_category_service(
    db: Session,
    current_user: User,
):
    current_date = datetime.now()

    start_date = datetime(current_date.year, current_date.month, 1)

    if current_date.month == 12:
        end_date = datetime(current_date.year + 1, 1, 1)
    else:
        end_date = datetime(current_date.year, current_date.month + 1, 1)

    result = (
        db.query(
            Category.category_name.label("category_name"),
            Category.category_color.label("category_color"),
            func.sum(Expense.expense_amount).label("total_amount"),
        )
        .join(Category, Expense.category_id == Category.id)
        .filter(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date,
        )
        .group_by(
            Category.id,
            Category.category_name,
            Category.category_color,
        )
        .order_by(func.sum(Expense.expense_amount).desc())
        .first()
    )

    if not result:
        return None

    return HighestCategoryResponse(
        category_name=result.category_name,
        category_color=result.category_color,
        total_amount=result.total_amount,
    )

def get_budget_progress_service(
    db: Session,
    current_user: User,
):
    current_date = datetime.now()

    start_date = datetime(current_date.year, current_date.month, 1)

    if current_date.month == 12:
        end_date = datetime(current_date.year + 1, 1, 1)
    else:
        end_date = datetime(current_date.year, current_date.month + 1, 1)

    total_spent = (
        db.query(
            func.coalesce(
                func.sum(Expense.expense_amount),
                0,
            )
        )
        .filter(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date,
        )
        .scalar()
    )

    return BudgetProgressResponse(
        monthly_income=current_user.monthly_income,
        total_spent=total_spent,
        remaining_balance=current_user.monthly_income - total_spent,
    )

def get_recurring_expenses_service(
    db: Session,
    current_user: User,
):
    results = (
        db.query(
            Expense.expense_name.label("expense_name"),
            func.count(Expense.id).label("total_occurrences"),
        )
        .filter(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
        )
        .group_by(
            Expense.expense_name,
        )
        .having(
            func.count(Expense.id) > 1
        )
        .order_by(
            func.count(Expense.id).desc()
        )
        .all()
    )

    recurring_expenses = [
        RecurringExpenseItem(
            expense_name=row.expense_name,
            total_occurrences=row.total_occurrences,
        )
        for row in results
    ]

    return RecurringExpenseResponse(
        recurring_expenses=recurring_expenses,
    )