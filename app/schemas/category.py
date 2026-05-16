from pydantic import BaseModel
from typing import Optional


class CategoryCreate(BaseModel):
    name:str
    budget: float | None = None


class CategoryResponse(BaseModel):
    id:int
    name:str
    budget: float | None = None
    total_spent: float = 0
    is_over_budget: bool = False

    class Config:
        from_attributes = True

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    budget: Optional[float] = None