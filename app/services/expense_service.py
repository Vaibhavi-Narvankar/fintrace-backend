from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate
from datetime import datetime

def create_expense_service(db:Session,expense: ExpenseCreate , user_id:int ):

    validate_category_ownership(
        db,
        expense.category_id,
        user_id
    )

    new_expense = Expense(
        expense_name=expense.expense_name,
        expense_amount=expense.expense_amount,
        expense_date=datetime.combine(
            expense.expense_date,
            datetime.min.time()
        ),
        payment_type=expense.payment_type,
        category_id=expense.category_id,
        user_id=user_id
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense


def validate_category_ownership(
        db: Session,
        category_id: int,
        user_id: int
):
    """
    🔒 Ensures category belongs to current user.
    Prevents cross-user access.
    """

    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == user_id,
        Category.is_deleted == False
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


def get_expense_service(db: Session, user_id: int):
    expenses = db.query(Expense).filter(
        Expense.is_deleted == False,
        Expense.user_id == user_id
    ).all()

    return expenses

def update_expense_service(db: Session,expense_id:int, expense_data: ExpenseUpdate, user_id:int):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id,
        Expense.is_deleted == False
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    update_data = expense_data.model_dump(exclude_unset=True)

    if "category_id" in update_data:
        validate_category_ownership(
            db,
            update_data["category_id"],
            user_id
        )

    # Convert date -> datetime if needed

    if "expense_date" in update_data:
        update_data["expense_date"] = datetime.combine(
            update_data["expense_date"],
            datetime.min.time()
        )

    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)
    return expense

def delete_expense_service(db: Session, expense_id:int, user_id:int):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == user_id,
        Expense.is_deleted == False
    ).first()

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    expense.is_deleted = True
    db.commit()
