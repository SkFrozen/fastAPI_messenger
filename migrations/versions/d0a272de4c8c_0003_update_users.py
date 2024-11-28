"""0003_update_users

Revision ID: d0a272de4c8c
Revises: c500816ad031
Create Date: 2024-11-27 17:20:53.958414

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0a272de4c8c'
down_revision: Union[str, None] = 'c500816ad031'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'last_name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    op.alter_column('users', 'first_name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)
    # ### end Alembic commands ###