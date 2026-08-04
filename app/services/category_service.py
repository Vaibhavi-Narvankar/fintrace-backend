from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Expense
from app.models.category import Category
from fastapi import HTTPException
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.core.exceptions import (
    NotFoundException,
    AlreadyExistsException,
)


async def get_user_categories_with_budget(
    db: AsyncSession,
    user_id: int
):
    statement = select(Category).where(
        Category.user_id == user_id,
        Category.is_deleted.is_(False),
    )

    result = await db.execute(statement)

    categories = result.scalars().all()

    response = []

    for category in categories:
        total_statement = select(
            func.sum(Expense.expense_amount)
        ).where(
            Expense.category_id == category.id,
            Expense.is_deleted.is_(False)
        )

        total_result = await db.execute(total_statement)
        total = total_result.scalar() or 0

        is_over = False

        if category.budget:
            is_over = total > category.budget

        response.append({
            "id": category.id,
            "name": category.name,
            "budget": float(category.budget) if category.budget else None,
            "total_spent": float(total),
            "is_over_budget": is_over,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        })

    return response

async def create_category_service(
    db: AsyncSession,
    category: CategoryCreate,
    user_id: int
):
    statement = select(Category).where(
        Category.name == category.name,
        Category.user_id == user_id,
        Category.is_deleted.is_(False)
    )

    result = await db.execute(statement)

    existing = result.scalars().first()

    if existing:
        raise AlreadyExistsException(
                "Category already exists"
            )

    new_category = Category(
        name=category.name,
        user_id=user_id
    )

    db.add(new_category)

    await db.commit()
    await db.refresh(new_category)

    return new_category

async def update_category_service(
    db: AsyncSession,
    category_id: int,
    category_data: CategoryUpdate,
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
        raise NotFoundException(
                "Category not found"
            )

    update_data = category_data.model_dump(
        exclude_unset=True
    )

    if "name" in update_data:

        existing_statement = select(Category).where(
            Category.name == update_data["name"],
            Category.user_id == user_id,
            Category.id != category_id,
            Category.is_deleted.is_(False)
        )

        existing_result = await db.execute(
            existing_statement
        )

        existing = existing_result.scalars().first()

        if existing:
            raise AlreadyExistsException(
                            "Category already exists"
                        )

    for field, value in update_data.items():
        setattr(category, field, value)

    await db.commit()
    await db.refresh(category)

    return category

async def delete_category_service(
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
        raise NotFoundException(
            "Category not found"
        )

    category.is_deleted = True

    await db.commit()

async def get_category_service(
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
        raise NotFoundException("Category not found"
        )

    return category
