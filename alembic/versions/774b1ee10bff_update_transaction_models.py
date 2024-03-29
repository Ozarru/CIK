"""update transaction models

Revision ID: 774b1ee10bff
Revises: c7fe1b60eacd
Create Date: 2023-02-08 18:37:59.008919

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '774b1ee10bff'
down_revision = 'c7fe1b60eacd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('other_bank_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('persona', sa.String(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('motive', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Integer(), nullable=True),
    sa.Column('due', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('other_cash_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('persona', sa.String(), nullable=True),
    sa.Column('fullname', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('motive', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Integer(), nullable=True),
    sa.Column('due', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('cashdesk_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['cashdesk_id'], ['cashdesks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient_bank_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Integer(), nullable=True),
    sa.Column('due', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patient_cash_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Integer(), nullable=True),
    sa.Column('due', sa.Integer(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('cashdesk_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['cashdesk_id'], ['cashdesks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bank_comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('cashdesk_comments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('user_bank_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('overview', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Integer(), nullable=True),
    sa.Column('due', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('bank_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_cash_transactions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('overview', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('paid', sa.Integer(), nullable=True),
    sa.Column('due', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.Column('cashdesk_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['cashdesk_id'], ['cashdesks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('bank_transactions')
    op.drop_table('cash_transactions')
    op.add_column('cashdesks', sa.Column('commentary', sa.String(), nullable=True))
    op.add_column('companies', sa.Column('insurance_id', sa.Integer(), nullable=True))
    op.drop_constraint('companies_inssurance_id_fkey', 'companies', type_='foreignkey')
    op.create_foreign_key(None, 'companies', 'insurances', ['insurance_id'], ['id'])
    op.drop_column('companies', 'inssurance_id')
    op.add_column('insurance_tiers', sa.Column('insurance_id', sa.Integer(), nullable=True))
    op.drop_constraint('insurance_tiers_inssurance_id_fkey', 'insurance_tiers', type_='foreignkey')
    op.create_foreign_key(None, 'insurance_tiers', 'insurances', ['insurance_id'], ['id'])
    op.drop_column('insurance_tiers', 'inssurance_id')
    op.add_column('transaction_genres', sa.Column('description', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transaction_genres', 'description')
    op.add_column('insurance_tiers', sa.Column('inssurance_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'insurance_tiers', type_='foreignkey')
    op.create_foreign_key('insurance_tiers_inssurance_id_fkey', 'insurance_tiers', 'insurances', ['inssurance_id'], ['id'])
    op.drop_column('insurance_tiers', 'insurance_id')
    op.add_column('companies', sa.Column('inssurance_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'companies', type_='foreignkey')
    op.create_foreign_key('companies_inssurance_id_fkey', 'companies', 'insurances', ['inssurance_id'], ['id'])
    op.drop_column('companies', 'insurance_id')
    op.drop_column('cashdesks', 'commentary')
    op.create_table('cash_transactions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('overview', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('paid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('due', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('cashdesk_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['cashdesk_id'], ['cashdesks.id'], name='cash_transactions_cashdesk_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], name='cash_transactions_genre_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='cash_transactions_pkey')
    )
    op.create_table('bank_transactions',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('overview', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cost', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('paid', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('due', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('bank_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('date', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['bank_id'], ['banks.id'], name='bank_transactions_bank_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['genre_id'], ['transaction_genres.id'], name='bank_transactions_genre_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='bank_transactions_pkey')
    )
    op.drop_table('user_cash_transactions')
    op.drop_table('user_bank_transactions')
    op.drop_table('cashdesk_comments')
    op.drop_table('bank_comments')
    op.drop_table('patient_cash_transactions')
    op.drop_table('patient_bank_transactions')
    op.drop_table('other_cash_transactions')
    op.drop_table('other_bank_transactions')
    # ### end Alembic commands ###
