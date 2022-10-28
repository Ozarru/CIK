"""fix pharmacy models

Revision ID: 14be25b877e1
Revises: 7e750c9b2551
Create Date: 2022-10-28 09:14:29.188111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14be25b877e1'
down_revision = '7e750c9b2551'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accessories', sa.Column('maker', sa.String(), nullable=True))
    op.add_column('accessories', sa.Column('unit_cost', sa.Integer(), nullable=False))
    op.drop_column('accessories', 'brand')
    op.add_column('medications', sa.Column('maker', sa.String(), nullable=True))
    op.add_column('medications', sa.Column('unit_cost', sa.Integer(), nullable=False))
    op.drop_column('medications', 'brand')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('medications', sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('medications', 'unit_cost')
    op.drop_column('medications', 'maker')
    op.add_column('accessories', sa.Column('brand', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('accessories', 'unit_cost')
    op.drop_column('accessories', 'maker')
    # ### end Alembic commands ###