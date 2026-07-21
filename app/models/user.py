from sqlalchemy import Column, Integer, String, DateTime, Boolean,Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    expenses = relationship("Expense", back_populates="user")
    categories = relationship("Category", back_populates="user")
    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    name = Column(String(100), nullable=True)
    profile_picture = Column(String, nullable=True)
    currency = Column(
        String(3),
        default="INR",
        server_default="INR",
        nullable=False
    )

    timezone = Column(
        String(50),
        default="Asia/Kolkata",
        server_default="Asia/Kolkata",
        nullable=False
    )
    monthly_income = Column(
        Numeric(10, 2),
        nullable=True
    )
    monthly_salary_date = Column(
            Integer,
            nullable=True
        )
