"""add use_ollama to users

Revision ID: c5a3b2f1d8e9
Revises: b46a2d9c7f10
Create Date: 2026-05-30 16:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c5a3b2f1d8e9"
down_revision: Union[str, Sequence[str], None] = "b46a2d9c7f10"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    result = conn.execute(sa.text("SHOW COLUMNS FROM users LIKE 'use_ollama'"))
    if result.fetchone() is None:
        op.add_column("users", sa.Column("use_ollama", sa.Boolean(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("users", "use_ollama")
