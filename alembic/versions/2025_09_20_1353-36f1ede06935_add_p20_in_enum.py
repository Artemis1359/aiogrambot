"""add_p20_in_enum

Revision ID: 36f1ede06935
Revises: f3ea681e9cfb
Create Date: 2025-09-20 13:53:00.552378

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '36f1ede06935'
down_revision: Union[str, None] = 'f3ea681e9cfb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE measurement ADD VALUE IF NOT EXISTS 'p20'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
