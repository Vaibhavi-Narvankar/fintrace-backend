from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.core.security import get_current_user
from app.models.user import User
from app.services.category_service import (
    get_user_categories_with_budget,
    create_category_service,
    update_category_service,
    delete_category_service,
    get_category_service
)

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(
        category:CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return create_category_service(
        db,
        category,
        current_user.id
    )

@router.get("/", response_model=list[CategoryResponse])
def get_categories(
        db: Session = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    return get_user_categories_with_budget(db, current_user.id)

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
        category_id : int,
        db: Session = Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    return get_category_service(
        db,
    category_id,
    current_user.id)

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
        category_id : int,
        category_data : CategoryUpdate,
        db:Session=Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    return update_category_service(db, category_id, category_data, current_user.id)


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id:int,
                    db:Session=Depends(get_db),
                    current_user: User = Depends(get_current_user)
                    ):
    return delete_category_service(db, category_id, current_user.id)


