from decimal import Decimal
from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.expense import Expense
from app.models.category import Category
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTrendResponse,
    TrendPoint,
    CategoryBreakdownItem,
    CategoryBreakdownResponse,
    HighestCategoryResponse,
    BudgetProgressResponse,
    RecurringExpenseItem,
    RecurringExpenseResponse,
)

async def get_dashboard_summary_service(
    db: AsyncSession,
    current_user: User
) -> DashboardSummaryResponse:

    expense_statement = select(
        func.coalesce(
            func.sum(Expense.expense_amount),
            0
        )
    ).where(
        Expense.user_id == current_user.id,
        Expense.is_deleted.is_(False)
    )

    expense_result = await db.execute(expense_statement)
    total_expense = expense_result.scalar()

    category_statement = select(
        func.count(Category.id)
    ).where(
        Category.user_id == current_user.id,
        Category.is_deleted.is_(False)
    )

    category_result = await db.execute(category_statement)
    total_categories = category_result.scalar()

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

async def get_dashboard_trends_service(
    db: AsyncSession,
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
            end_date = datetime(
                current_date.year + 1,
                1,
                1
            )
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

    period_column = func.date_trunc(
        group_by_unit,
        Expense.expense_date
    ).label("period")

    statement = (
        select(
            period_column,
            func.coalesce(
                func.sum(Expense.expense_amount),
                0
            ).label("amount")
        )
        .where(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date
        )
        .group_by(period_column)
        .order_by(period_column)
    )

    result = await db.execute(statement)
    results = result.all()

    trends = [
        TrendPoint(
            label=(
                row.period.strftime("%b")
                if period == "yearly"
                else row.period.strftime("%d %b")
            ),
            amount=row.amount
        )
        for row in results
    ]

    return DashboardTrendResponse(
        trends=trends
    )

async def get_category_breakdown_service(
    db: AsyncSession,
    current_user: User,
):
    current_date = datetime.now()

    start_date = datetime(
        current_date.year,
        current_date.month,
        1
    )

    if current_date.month == 12:
        end_date = datetime(
            current_date.year + 1,
            1,
            1
        )
    else:
        end_date = datetime(
            current_date.year,
            current_date.month + 1,
            1
        )

    statement = (
        select(
            Category.name.label("category_name"),
            Category.color.label("category_color"),
            func.coalesce(
                func.sum(Expense.expense_amount),
                0
            ).label("total_amount")
        )
        .join(
            Category,
            Expense.category_id == Category.id
        )
        .where(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            Category.is_deleted.is_(False),
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date,
        )
        .group_by(
            Category.id,
            Category.name,
            Category.color,
        )
        .order_by(
            func.sum(Expense.expense_amount).desc()
        )
    )

    result = await db.execute(statement)
    results = result.all()

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


async def get_highest_category_service(
    db: AsyncSession,
    current_user: User,
):
    current_date = datetime.now()

    start_date = datetime(
        current_date.year,
        current_date.month,
        1
    )

    if current_date.month == 12:
        end_date = datetime(
            current_date.year + 1,
            1,
            1
        )
    else:
        end_date = datetime(
            current_date.year,
            current_date.month + 1,
            1
        )

    statement = (
        select(
            Category.name.label("name"),
            Category.color.label("color"),
            func.sum(
                Expense.expense_amount
            ).label("total_amount"),
        )
        .join(
            Category,
            Expense.category_id == Category.id
        )
        .where(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
            Category.is_deleted.is_(False),
            Expense.expense_date >= start_date,
            Expense.expense_date < end_date,
        )
        .group_by(
            Category.id,
            Category.name,
            Category.color,
        )
        .order_by(
            func.sum(
                Expense.expense_amount
            ).desc()
        )
        .limit(1)
    )

    db_result = await db.execute(statement)
    result = db_result.first()

    if not result:
        return None

    return HighestCategoryResponse(
        category_name=result.name,
        category_color=result.color,
        total_amount=result.total_amount,
    )

async def get_budget_progress_service(
    db: AsyncSession,
    current_user: User,
):
    current_date = datetime.now()

    start_date = datetime(
        current_date.year,
        current_date.month,
        1
    )

    if current_date.month == 12:
        end_date = datetime(
            current_date.year + 1,
            1,
            1
        )
    else:
        end_date = datetime(
            current_date.year,
            current_date.month + 1,
            1
        )

    statement = select(
        func.coalesce(
            func.sum(Expense.expense_amount),
            0,
        )
    ).where(
        Expense.user_id == current_user.id,
        Expense.is_deleted.is_(False),
        Expense.expense_date >= start_date,
        Expense.expense_date < end_date,
    )

    result = await db.execute(statement)
    total_spent = result.scalar()

    monthly_income = current_user.monthly_income or Decimal("0")

    return BudgetProgressResponse(
        monthly_income=monthly_income,
        total_spent=total_spent,
        remaining_balance=monthly_income - total_spent,
    )


async def get_recurring_expenses_service(
    db: AsyncSession,
    current_user: User,
):
    count_column = func.count(
        Expense.id
    ).label("total_occurrences")

    statement = (
        select(
            Expense.expense_name.label("expense_name"),
            count_column,
        )
        .where(
            Expense.user_id == current_user.id,
            Expense.is_deleted.is_(False),
        )
        .group_by(
            Expense.expense_name,
        )
        .having(
            func.count(Expense.id) > 1,
        )
        .order_by(
            count_column.desc(),
        )
    )

    result = await db.execute(statement)
    results = result.all()

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