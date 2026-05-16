from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime, date
from typing import Optional


class ExpenseCreate(BaseModel):
    expense_name:str
    expense_amount:Decimal
    expense_date:date
    payment_type:str
    category_id:int

class ExpenseResponse(BaseModel):
    id:int
    expense_name:str
    expense_amount:Decimal
    expense_date:datetime
    payment_type:str
    created_at:datetime

    class Config:
        from_attributes = True

class ExpenseUpdate(BaseModel):
    expense_name: Optional[str] = None
    expense_amount: Optional[float] = None
    expense_date: Optional[date] = None
    payment_type: Optional[str] = None
    category_id: Optional[int] = None
