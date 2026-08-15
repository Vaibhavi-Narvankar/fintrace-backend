"""add bank transactions

Revision ID: a734556d15a6
Revises: 1104e85fc18d
Create Date: 2026-08-15 08:38:39.776415

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a734556d15a6"
down_revision: Union[str, Sequence[str], None] = "1104e85fc18d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bank_transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("statement_id", sa.Integer(), nullable=False),
        sa.Column("transaction_date", sa.Date(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column(
            "debit_amount",
            sa.Numeric(precision=12, scale=2),
            nullable=True
        ),
        sa.Column(
            "credit_amount",
            sa.Numeric(precision=12, scale=2),
            nullable=True
        ),
        sa.Column(
            "balance",
            sa.Numeric(precision=12, scale=2),
            nullable=True
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["statement_id"],
            ["bank_statements.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_bank_transactions_id",
        "bank_transactions",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_bank_transactions_statement_id",
        "bank_transactions",
        ["statement_id"],
        unique=False
    )


def downgrade() -> None:
    op.drop_index(
        "ix_bank_transactions_statement_id",
        table_name="bank_transactions"
    )

    op.drop_index(
        "ix_bank_transactions_id",
        table_name="bank_transactions"
    )

    op.drop_table("bank_transactions")