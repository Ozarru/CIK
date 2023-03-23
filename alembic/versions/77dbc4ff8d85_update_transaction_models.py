"""update transaction models

Revision ID: 77dbc4ff8d85
Revises: 74f662f05c5e
Create Date: 2023-02-21 13:36:52.533675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77dbc4ff8d85'
down_revision = '74f662f05c5e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_genres')
    op.add_column('bills', sa.Column('due', sa.Integer(), nullable=False))
    op.drop_column('bills', 'balance')
    op.add_column('other_bank_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('other_bank_transactions_genre_id_fkey',
                       'other_bank_transactions', type_='foreignkey')
    op.drop_column('other_bank_transactions', 'genre_id')
    op.add_column('other_cash_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('other_cash_transactions_genre_id_fkey',
                       'other_cash_transactions', type_='foreignkey')
    op.drop_column('other_cash_transactions', 'genre_id')
    op.add_column('other_mobile_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('other_mobile_transactions_genre_id_fkey',
                       'other_mobile_transactions', type_='foreignkey')
    op.drop_column('other_mobile_transactions', 'genre_id')
    op.add_column('patient_bank_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('patient_bank_transactions_genre_id_fkey',
                       'patient_bank_transactions', type_='foreignkey')
    op.drop_column('patient_bank_transactions', 'genre_id')
    op.add_column('patient_cash_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('patient_cash_transactions_genre_id_fkey',
                       'patient_cash_transactions', type_='foreignkey')
    op.drop_column('patient_cash_transactions', 'genre_id')
    op.add_column('patient_mobile_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('patient_mobile_transactions_genre_id_fkey',
                       'patient_mobile_transactions', type_='foreignkey')
    op.drop_column('patient_mobile_transactions', 'genre_id')
    op.add_column('user_bank_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('user_bank_transactions_genre_id_fkey',
                       'user_bank_transactions', type_='foreignkey')
    op.drop_column('user_bank_transactions', 'genre_id')
    op.add_column('user_cash_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('user_cash_transactions_genre_id_fkey',
                       'user_cash_transactions', type_='foreignkey')
    op.drop_column('user_cash_transactions', 'genre_id')
    op.add_column('user_mobile_transactions', sa.Column(
        'genre', sa.String(), nullable=False))
    op.drop_constraint('user_mobile_transactions_genre_id_fkey',
                       'user_mobile_transactions', type_='foreignkey')
    op.drop_column('user_mobile_transactions', 'genre_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_mobile_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_mobile_transactions_genre_id_fkey', 'user_mobile_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('user_mobile_transactions', 'genre')
    op.add_column('user_cash_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_cash_transactions_genre_id_fkey', 'user_cash_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('user_cash_transactions', 'genre')
    op.add_column('user_bank_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('user_bank_transactions_genre_id_fkey', 'user_bank_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('user_bank_transactions', 'genre')
    op.add_column('patient_mobile_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('patient_mobile_transactions_genre_id_fkey', 'patient_mobile_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('patient_mobile_transactions', 'genre')
    op.add_column('patient_cash_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('patient_cash_transactions_genre_id_fkey', 'patient_cash_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('patient_cash_transactions', 'genre')
    op.add_column('patient_bank_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('patient_bank_transactions_genre_id_fkey', 'patient_bank_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('patient_bank_transactions', 'genre')
    op.add_column('other_mobile_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('other_mobile_transactions_genre_id_fkey', 'other_mobile_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('other_mobile_transactions', 'genre')
    op.add_column('other_cash_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('other_cash_transactions_genre_id_fkey', 'other_cash_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('other_cash_transactions', 'genre')
    op.add_column('other_bank_transactions', sa.Column(
        'genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('other_bank_transactions_genre_id_fkey', 'other_bank_transactions',
                          'transaction_genres', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_column('other_bank_transactions', 'genre')
    op.add_column('bills', sa.Column('balance', sa.INTEGER(),
                  autoincrement=False, nullable=False))
    op.drop_column('bills', 'due')
    op.create_table('transaction_genres',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.Column('description', sa.VARCHAR(),
                              autoincrement=False, nullable=False),
                    sa.PrimaryKeyConstraint(
                        'id', name='transaction_genres_pkey'),
                    sa.UniqueConstraint(
                        'name', name='transaction_genres_name_key')
                    )
    # ### end Alembic commands ###