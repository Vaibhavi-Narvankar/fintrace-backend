from sqlalchemy import DateTime, Column, Integer ,String, ForeignKey, Numeric, Boolean
from datetime import datetime, timezone
from app.db.base import Base
from sqlalchemy.orm import relationship


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    expense_name = Column(String, nullable=False)
    expense_amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(DateTime, nullable=False)
    payment_type = Column(String, nullable=False)
    is_auto_fetched = Column(Boolean, default=False)
    tax_percent = Column(Numeric(5, 2), nullable=True)
    tax_amount = Column(Numeric(10, 2), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")