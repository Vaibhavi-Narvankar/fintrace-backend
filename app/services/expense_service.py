from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.category import Category


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
        Category.user_id == user_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category