"""add fin models

Revision ID: 9c3f79b411f6
Revises: 4fd1435834ee
Create Date: 2022-10-27 11:52:35.194081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c3f79b411f6'
down_revision = '4fd1435834ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('insurances',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bills',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date_issued', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('date_due', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('genre', sa.String(), nullable=False),
    sa.Column('total', sa.Integer(), nullable=False),
    sa.Column('paid', sa.Integer(), nullable=False),
    sa.Column('balance', sa.Integer(), nullable=False),
    sa.Column('is_paid', sa.Boolean(), server_default='False', nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('insurance_tiers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('percentage', sa.Float(), nullable=False),
    sa.Column('inssurance_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['inssurance_id'], ['insurances.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('salaries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('qualification', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('wages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hourly_rate', sa.Integer(), nullable=False),
    sa.Column('qualification', sa.String(), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pay_salaries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('month', sa.String(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pay_wages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('hourly_rate', sa.Integer(), nullable=False),
    sa.Column('hours_worked', sa.Float(), nullable=False),
    sa.Column('month', sa.String(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pay_wages')
    op.drop_table('pay_salaries')
    op.drop_table('wages')
    op.drop_table('salaries')
    op.drop_table('insurance_tiers')
    op.drop_table('bills')
    op.drop_table('insurances')
    # ### end Alembic commands ###