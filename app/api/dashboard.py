from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.dashboard import DashboardSummaryResponse
from app.services.dashboard_service import (get_dashboard_summary_service,get_dashboard_trends_service,get_category_breakdown_service,
get_highest_category_service,get_budget_progress_service,get_recurring_expenses_service)
from app.schemas.dashboard import (CategoryBreakdownResponse,HighestCategoryResponse,BudgetProgressResponse,RecurringExpenseResponse,
CategoryBreakdownResponse,BudgetProgressResponse, DashboardTrendResponse)
from app.schemas.common_response_schema import ApiResponse

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/summary", response_model=ApiResponse[DashboardSummaryResponse])
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_dashboard_summary_service(db=db, current_user=current_user)
    return ApiResponse(
        message="Dashboard summary fetched successfully",
        data=result
    )

@router.get("/trends", response_model=ApiResponse[DashboardTrendResponse])
async def get_dashboard_trends(
    period: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_dashboard_trends_service(
        db=db,
        current_user=current_user,
        period=period
    )
    return ApiResponse(
        message="Dashboard trends fetched successfully",
        data=result
    )

@router.get("/category-breakdown", response_model=ApiResponse[CategoryBreakdownResponse])
async def get_category_breakdown(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_category_breakdown_service(
        db=db,
        current_user=current_user
    )
    return ApiResponse(
        message="Category breakdown fetched successfully",
        data=result
    )

@router.get("/highest-category", response_model=ApiResponse[HighestCategoryResponse | None])
async def get_highest_category(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_highest_category_service(db, current_user)
    return ApiResponse(
        message="Highest spending category fetched successfully",
        data=result
    )

@router.get("/budget-progress", response_model=ApiResponse[BudgetProgressResponse])
async def get_budget_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_budget_progress_service(db, current_user)
    return ApiResponse(
        message="Budget progress fetched successfully",
        data=result
    )

@router.get("/recurring-expenses", response_model=ApiResponse[RecurringExpenseResponse])
async def get_recurring_expenses(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_recurring_expenses_service(db, current_user)
    return ApiResponse(
        message="Recurring expenses fetched successfully",
        data=result
    )