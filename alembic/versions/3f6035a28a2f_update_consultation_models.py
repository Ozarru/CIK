"""update consultation models

Revision ID: 3f6035a28a2f
Revises: 8119ccdc8046
Create Date: 2023-01-06 17:49:29.354383

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f6035a28a2f'
down_revision = '8119ccdc8046'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consultation_genres', sa.Column('price', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('consultation_genres', 'price')
    # ### end Alembic commands ###