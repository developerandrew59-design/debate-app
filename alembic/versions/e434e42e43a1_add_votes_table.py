"""add votes table

Revision ID: e434e42e43a1
Revises: e675d7781b2f
Create Date: 2026-06-25 11:25:15.797094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e434e42e43a1'
down_revision: Union[str, Sequence[str], None] = 'e675d7781b2f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "votes",
        sa.Column('id',sa.Integer(),nullable=False),
        sa.Column('vote',sa.Boolean(),nullable=False),
        sa.Column('account_id',sa.Integer,nullable=False),
        sa.Column('argument_id',sa.Integer,nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default='now()', nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['account_id'], ['accounts.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['argument_id'], ['arguments.id'], ondelete='CASCADE'),

    )
    


def downgrade() -> None:
    op.drop_table('votes')
    
