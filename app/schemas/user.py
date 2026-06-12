from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str