from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import Expense
from app.models.category import Category
from fastapi import HTTPException
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_user_categories_with_budget(db:Session,user_id:int):
    categories = db.query(Category).filter(
        Category.user_id == user_id,
        Category.is_deleted == False,
    ).all()

    result = []

    for category in categories:
        total = db.query(func.sum(Expense.expense_amount)).filter(
            Expense.category_id == category.id,
            Expense.is_deleted == False
        ).scalar() or 0

        is_over = False
        if category.budget:
           is_over = total > category.budget


        result.append({
            "id": category.id,
            "name": category.name,
            "budget": float(category.budget) if category.budget else None,
            "total_spent": float(total),
            "is_over_budget": is_over
        })

    return result

def create_category_service(db: Session,
    category: CategoryCreate,
    user_id: int
    ):
        existing = db.query(Category).filter(
            Category.name == category.name,
            Category.user_id == user_id,
            Category.is_deleted == False
        ).first()

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Category already exists"
            )

        new_category = Category(
            name=category.name,
            user_id=user_id
        )

        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category

def update_category_service(
        db: Session,
        category_id: int,
        category_data: CategoryUpdate,
        user_id: int
):
                category = db.query(Category).filter(Category.id == category_id, Category.user_id == user_id,
                                                     Category.is_deleted == False).first()

                existing = db.query(Category).filter(
                    Category.name == category_data.name,
                    Category.user_id == user_id,
                    Category.id != category_id,
                    Category.is_deleted == False
                ).first()

                if existing:
                    raise HTTPException(status_code=400, detail="Category already exists")

                if not category:
                    raise HTTPException(status_code=404, detail="Category not found")

                if category_data.name is not None:
                    category.name = category_data.name

                if category_data.budget is not None:
                    category.budget = category_data.budget

                db.commit()
                db.refresh(category)

                return category

def delete_category_service(
    db: Session,
    category_id: int,
    user_id: int
):
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

    category.is_deleted = True

    db.commit()

def get_category_service(
            db: Session,
            category_id: int,
            user_id: int
    ):
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
