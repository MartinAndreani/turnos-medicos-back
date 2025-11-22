"""insert datos

Revision ID: d9fee4b33ec3
Revises: a27c2313e139
Create Date: 2025-11-22 17:10:14.490591

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9fee4b33ec3'
down_revision: Union[str, Sequence[str], None] = 'a27c2313e139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
