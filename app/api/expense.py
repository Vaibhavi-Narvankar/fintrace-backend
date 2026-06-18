from datetime import datetime
from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.models.expense import Expense
from app.db.session import get_db
from app.schemas.expense import ExpenseResponse, ExpenseCreate, ExpenseUpdate
from app.services.expense_service import validate_category_ownership


router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseResponse)
def create_expense(
        expense:ExpenseCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    existing = db.query(Expense).filter(Expense.expense_name == expense.expense_name, Expense.user_id == current_user.id, Expense.is_deleted == False).first()

    if existing:
        raise HTTPException(status_code=400, detail="Expense already exists")

    validate_category_ownership(
        db,
        expense.category_id,
        current_user.id
    )

    new_expense = Expense(
        expense_name = expense.expense_name,
        expense_amount = expense.expense_amount,
        expense_date=datetime.combine(
            expense.expense_date,
            datetime.min.time()
        ),
        payment_type = expense.payment_type,
        category_id = expense.category_id,
        user_id = current_user.id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.get("/", response_model=list[ExpenseResponse])
def get_expenses(
        db : Session = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    expenses = db.query(Expense).filter(
        Expense.is_deleted == False,
        Expense.user_id == current_user.id
    ).all()

    return expenses


@router.patch("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
        expense_id: int,
        expense_data: ExpenseUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # 🔹 update only provided fields
    if expense_data.expense_name is not None:
        expense.expense_name = expense_data.expense_name

    if expense_data.expense_amount is not None:
        expense.expense_amount = expense_data.expense_amount

    if expense_data.expense_date is not None:
        expense.expense_date = datetime.combine(
            expense_data.expense_date,
            datetime.min.time()
        )

    if expense_data.payment_type is not None:
        expense.payment_type = expense_data.payment_type

    if expense_data.category_id is not None:
        validate_category_ownership(
            db,
            expense_data.category_id,
            current_user.id
        )

        expense.category_id = expense_data.category_id

    db.commit()
    db.refresh(expense)

    return expense

@router.delete("/{expense_id}", status_code=204)
def delete_expense(
        expense_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id,
        Expense.is_deleted == False
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.is_deleted = True
    db.commit()


