from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.core.security import get_current_user
from app.models.user import User
from app.services.category_service import get_user_categories_with_budget

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(
        category:CategoryCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    existing = db.query(Category).filter(Category.name == category.name, Category.user_id == current_user.id).first()

    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")

    new_category = Category(
        name = category.name,
        user_id = current_user.id
    )

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category

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
    category = db.query(Category).filter(Category.id==category_id,Category.user_id==current_user.id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category

@router.patch("/{category_id}", response_model=CategoryResponse)
def update_category(
        category_id : int,
        category_data : CategoryUpdate,
        db:Session=Depends(get_db),
        current_user : User = Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()

    existing = db.query(Category).filter(
        Category.name == category_data.name,
        Category.user_id == current_user.id,
        Category.id != category_id
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


@router.delete("/{category_id}", status_code=204)
def delete_category(category_id:int,
                    db:Session=Depends(get_db),
                    current_user: User = Depends(get_current_user)
                    ):
    category = db.query(Category).filter(Category.id == category_id,
                                         Category.user_id == current_user.id).first()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    db.delete(category)
    db.commit()


