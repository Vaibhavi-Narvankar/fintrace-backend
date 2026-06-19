from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db
from app.schemas.expense import ExpenseResponse, ExpenseCreate, ExpenseUpdate
from app.services.expense_service import ( create_expense_service, get_expense_service, update_expense_service, delete_expense_service)


router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense(
        expense:ExpenseCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
     return create_expense_service(db, expense, current_user.id)

@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
        db : Session = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    return get_expense_service(db, current_user.id)

@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
        expense_id: int,
        expense_data: ExpenseUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return update_expense_service(db, expense_id, expense_data, current_user.id)

@router.delete("/{expense_id}", status_code=204)
def delete_expense(
        expense_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return delete_expense_service(db, expense_id, current_user.id)


