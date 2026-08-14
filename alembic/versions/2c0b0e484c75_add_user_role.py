"""add user role

Revision ID: 2c0b0e484c75
Revises: e7d4308e5f01
Create Date: 2026-08-14 05:30:08.668757

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2c0b0e484c75"
down_revision: Union[str, Sequence[str], None] = "e7d4308e5f01"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    role_enum = sa.Enum(
        "user",
        "admin",
        name="user_role"
    )

    role_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "users",
        sa.Column(
            "role",
            role_enum,
            nullable=True
        )
    )

    op.execute(
        "UPDATE users SET role = 'user' WHERE role IS NULL"
    )

    op.alter_column(
        "users",
        "role",
        nullable=False
    )


def downgrade() -> None:
    op.drop_column("users", "role")

    role_enum = sa.Enum(
        "USER",
        "ADMIN",
        name="user_role"
    )

    role_enum.drop(op.get_bind(), checkfirst=True)
