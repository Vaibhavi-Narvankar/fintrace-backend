from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db
from app.schemas.expense import ExpenseResponse, ExpenseCreate, ExpenseUpdate
from app.services.expense_service import ( create_expense_service, get_expense_service, update_expense_service, delete_expense_service)
from app.schemas.common_response_schema import ApiResponse


router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ApiResponse[ExpenseResponse])
async def create_expense(
        expense:ExpenseCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
     result = await create_expense_service(
             db,
             expense,
             current_user.id
         )

     return ApiResponse(
             success=True,
             message="Expense created successfully",
             data=result
         )

@router.get("/", response_model=ApiResponse[list[ExpenseResponse]])
async def get_expenses(
        db : AsyncSession = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    result = await get_expense_service(db, current_user.id)

    return ApiResponse(message="Expenses fetched successfully",data=result)

@router.patch("/{expense_id}", response_model=ApiResponse[ExpenseResponse])
async def update_expense(
        expense_id: int,
        expense_data: ExpenseUpdate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await update_expense_service(db, expense_id, expense_data, current_user.id)
    return ApiResponse(message="Expense updated successfully",data=result)

@router.delete("/{expense_id}",response_model=ApiResponse[None])
async def delete_expense(
        expense_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    await delete_expense_service(db, expense_id, current_user.id)
    return ApiResponse(
            message="Expense deleted successfully",
            data=None
        )


