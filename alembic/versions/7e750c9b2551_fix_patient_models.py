"""fix patient models

Revision ID: 7e750c9b2551
Revises: 6934b58a13f9
Create Date: 2022-10-27 13:34:20.767571

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e750c9b2551'
down_revision = '6934b58a13f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('patients', 'matrimony',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('patients', 'code')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('code', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.alter_column('patients', 'matrimony',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
