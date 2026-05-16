from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models import Expense
from app.db.models.category import Category


def get_user_categories_with_budget(db:Session,user_id:int):
    categories = db.query(Category).filter(
        Category.user_id == user_id
    ).all()

    result = []

    for category in categories:
        total = db.query(func.sum(Expense.expense_amount)).filter(
            Expense.category_id == category.id
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