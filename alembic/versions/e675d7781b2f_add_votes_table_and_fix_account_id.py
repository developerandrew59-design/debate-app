"""add votes table and fix account_id

Revision ID: e675d7781b2f
Revises: 412ac409ef8c
Create Date: 2026-06-24 23:21:44.831109

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e675d7781b2f'
down_revision: Union[str, Sequence[str], None] = '412ac409ef8c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("arguments","account_id",nullable=False)
    


def downgrade() -> None:
    op.alter_column("arguments", "account_id", nullable=True)
    
    
