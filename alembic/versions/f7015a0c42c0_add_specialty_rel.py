"""add specialty rel

Revision ID: f7015a0c42c0
Revises: 9b302dbcd4e0
Create Date: 2022-11-07 10:43:00.378599

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7015a0c42c0'
down_revision = '9b302dbcd4e0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'specialties', ['id'])
    op.add_column('users', sa.Column('specialty_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'specialties', ['specialty_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'specialty_id')
    op.drop_constraint(None, 'specialties', type_='unique')
    # ### end Alembic commands ###
