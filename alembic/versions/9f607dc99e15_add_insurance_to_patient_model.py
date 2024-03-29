"""add insurance to patient model

Revision ID: 9f607dc99e15
Revises: 63113af827d4
Create Date: 2023-02-13 13:10:23.186904

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f607dc99e15'
down_revision = '63113af827d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patients', sa.Column('is_insurred', sa.Boolean(), server_default='false', nullable=True))
    op.add_column('patients', sa.Column('isurance_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'patients', 'insurances', ['isurance_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'patients', type_='foreignkey')
    op.drop_column('patients', 'isurance_id')
    op.drop_column('patients', 'is_insurred')
    # ### end Alembic commands ###
