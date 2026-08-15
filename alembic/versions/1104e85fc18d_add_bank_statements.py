"""add bank statements

Revision ID: 1104e85fc18d
Revises: 2c0b0e484c75
Create Date: 2026-08-15 08:06:04.005324

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "1104e85fc18d"
down_revision: Union[str, Sequence[str], None] = "2c0b0e484c75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    statement_status_enum = sa.Enum(
        "uploaded",
        "processing",
        "completed",
        "failed",
        name="statement_status"
    )

    op.create_table(
        "bank_statements",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("file_name", sa.String(), nullable=False),
        sa.Column(
            "statement_start_date",
            sa.Date(),
            nullable=True
        ),
        sa.Column(
            "statement_end_date",
            sa.Date(),
            nullable=True
        ),
        sa.Column(
            "status",
            statement_status_enum,
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"]
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "ix_bank_statements_id",
        "bank_statements",
        ["id"],
        unique=False
    )

    op.create_index(
        "ix_bank_statements_user_id",
        "bank_statements",
        ["user_id"],
        unique=False
    )

def downgrade() -> None:
    op.drop_index(
        "ix_bank_statements_user_id",
        table_name="bank_statements"
    )

    op.drop_index(
        "ix_bank_statements_id",
        table_name="bank_statements"
    )

    op.drop_table("bank_statements")

    statement_status_enum = sa.Enum(
        "uploaded",
        "processing",
        "completed",
        "failed",
        name="statement_status"
    )

    statement_status_enum.drop(
        op.get_bind(),
        checkfirst=True
    )