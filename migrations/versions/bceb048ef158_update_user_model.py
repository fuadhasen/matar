"""update user model

Revision ID: bceb048ef158
Revises: 4df52f39fc77
Create Date: 2025-01-02 01:31:21.653276

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'bceb048ef158'
down_revision: Union[str, None] = '4df52f39fc77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_column('user', 'hashed_password')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('hashed_password', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('user', 'password')
    # ### end Alembic commands ###