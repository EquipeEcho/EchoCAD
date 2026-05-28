"""add user groq api key

Revision ID: b46a2d9c7f10
Revises: a315325366fd
Create Date: 2026-05-28 17:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b46a2d9c7f10"
down_revision: Union[str, Sequence[str], None] = "a315325366fd"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("groq_api_key_encrypted", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "groq_api_key_encrypted")
