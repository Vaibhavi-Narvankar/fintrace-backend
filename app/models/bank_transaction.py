from sqlalchemy import (
     Column,
     Integer,
     String,
     Date,
     DateTime,
     ForeignKey,
     Numeric,
 )
from sqlalchemy.sql import func

from app.db.base import Base


class BankTransaction(Base):
     __tablename__ = "bank_transactions"

     id = Column(
         Integer,
         primary_key=True,
         index=True
     )

     statement_id = Column(
         Integer,
         ForeignKey("bank_statements.id"),
         nullable=False,
         index=True
     )

     transaction_date = Column(
         Date,
         nullable=False
     )

     description = Column(
         String,
         nullable=False
     )

     debit_amount = Column(
         Numeric(12, 2),
         nullable=True
     )

     credit_amount = Column(
         Numeric(12, 2),
         nullable=True
     )

     balance = Column(
         Numeric(12, 2),
         nullable=True
     )

     created_at = Column(
         DateTime(timezone=True),
         server_default=func.now(),
         nullable=False
     )