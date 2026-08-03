from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.category import Category
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


async def validate_category_ownership(
    db: AsyncSession,
    category_id: int,
    user_id: int
):
    statement = select(Category).where(
        Category.id == category_id,
        Category.user_id == user_id,
        Category.is_deleted.is_(False)
    )

    result = await db.execute(statement)
    category = result.scalars().first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category

async def create_expense_service(
    db: AsyncSession,
    expense: ExpenseCreate,
    user_id: int
):
    await validate_category_ownership(
        db=db,
        category_id=expense.category_id,
        user_id=user_id
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

    await db.commit()
    await db.refresh(new_expense)

    return new_expense

async def get_expense_service(
    db: AsyncSession,
    user_id: int
):
    statement = select(Expense).where(
        Expense.is_deleted.is_(False),
        Expense.user_id == user_id
    )

    result = await db.execute(statement)

    expenses = result.scalars().all()

    return expenses

async def update_expense_service(
    db: AsyncSession,
    expense_id: int,
    expense_data: ExpenseUpdate,
    user_id: int
):
    statement = select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == user_id,
        Expense.is_deleted.is_(False)
    )

    result = await db.execute(statement)
    expense = result.scalars().first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    update_data = expense_data.model_dump(
        exclude_unset=True
    )

    if "category_id" in update_data:
        await validate_category_ownership(
            db=db,
            category_id=update_data["category_id"],
            user_id=user_id
        )

    if "expense_date" in update_data:
        update_data["expense_date"] = datetime.combine(
            update_data["expense_date"],
            datetime.min.time()
        )

    for field, value in update_data.items():
        setattr(expense, field, value)

    await db.commit()
    await db.refresh(expense)

    return expense

async def delete_expense_service(
    db: AsyncSession,
    expense_id: int,
    user_id: int
):
    statement = select(Expense).where(
        Expense.id == expense_id,
        Expense.user_id == user_id,
        Expense.is_deleted.is_(False)
    )

    result = await db.execute(statement)
    expense = result.scalars().first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense.is_deleted = True

    await db.commit()
