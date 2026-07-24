from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import (get_dashboard_summary_service,get_dashboard_trends_service,get_category_breakdown_service,
get_highest_category_service,get_budget_progress_service,get_recurring_expenses_service)
from app.schemas.dashboard import (CategoryBreakdownResponse,HighestCategoryResponse,BudgetProgressResponse,RecurringExpenseResponse,
CategoryBreakdownResponse,BudgetProgressResponse)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get(
    "/summary",
    response_model=DashboardSummaryResponse
)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_summary_service(
        db=db,
        current_user=current_user
    )

@router.get("/trends")
def get_dashboard_trends(
    period: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_dashboard_trends_service(
        db=db,
        current_user=current_user,
        period=period
    )

@router.get(
    "/category-breakdown",
    response_model=CategoryBreakdownResponse,
)
def get_category_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_category_breakdown_service(
        db=db,
        current_user=current_user,
    )

@router.get(
    "/highest-category",
    response_model=HighestCategoryResponse | None,
)
def get_highest_category(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_highest_category_service(db, current_user)

@router.get(
    "/budget-progress",
    response_model=BudgetProgressResponse,
)
def get_budget_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_budget_progress_service(
        db,
        current_user,
    )

@router.get(
    "/recurring-expenses",
    response_model=RecurringExpenseResponse,
)
def get_recurring_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_recurring_expenses_service(
        db,
        current_user,
    )