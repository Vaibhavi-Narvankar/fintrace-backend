from sqlalchemy import Column, Integer, String, ForeignKey,Boolean, Numeric, DateTime
from app.db.base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"),index=True)
    name = Column(String(50), nullable=False, unique=True)
    color = Column(String(50), nullable=True)
    budget = Column(Numeric(10, 2), nullable=True)
    expenses = relationship("Expense", back_populates="category")
    user = relationship("User", back_populates="categories")
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



