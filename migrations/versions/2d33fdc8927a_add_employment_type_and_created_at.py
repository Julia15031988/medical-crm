"""add employment type and created at

Revision ID: 2d33fdc8927a
Revises: cb224e7fcef2
Create Date: 2026-07-04 12:49:57.665888
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "2d33fdc8927a"
down_revision: Union[str, Sequence[str], None] = "cb224e7fcef2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    employment_type_enum = sa.Enum(
        "FULL_TIME",
        "PART_TIME",
        name="employment_type",
    )
    employment_type_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "appointments",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    op.add_column(
        "doctor_profiles",
        sa.Column(
            "employment_type",
            employment_type_enum,
            server_default="FULL_TIME",
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("doctor_profiles", "employment_type")
    op.drop_column("appointments", "created_at")

    employment_type_enum = sa.Enum(
        "FULL_TIME",
        "PART_TIME",
        name="employment_type",
    )
    employment_type_enum.drop(op.get_bind(), checkfirst=True)
