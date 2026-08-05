from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
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
from app.schemas.common_response_schema import ApiResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=ApiResponse[CategoryResponse])
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await create_category_service(db, category, current_user.id)
    return ApiResponse(
        message="Category created successfully",
        data=result
    )

@router.get("/", response_model=ApiResponse[list[CategoryResponse]])
async def get_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_user_categories_with_budget(db, current_user.id)
    return ApiResponse(
        message="Categories fetched successfully",
        data=result
    )

@router.get("/{category_id}", response_model=ApiResponse[CategoryResponse])
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await get_category_service(db, category_id, current_user.id)
    return ApiResponse(
        message="Category fetched successfully",
        data=result
    )

@router.patch("/{category_id}", response_model=ApiResponse[CategoryResponse])
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await update_category_service(
        db, category_id, category_data, current_user.id
    )
    return ApiResponse(
        message="Category updated successfully",
        data=result
    )

@router.delete("/{category_id}", response_model=ApiResponse[None])
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await delete_category_service(db, category_id, current_user.id)
    return ApiResponse(
        message="Category deleted successfully",
        data=None
    )


