"""Init

Revision ID: 249e7b4ed960
Revises: 
Create Date: 2022-10-13 02:24:51.278122

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '249e7b4ed960'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accounts',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_accounts_id'), 'accounts', ['id'], unique=False)
    op.create_index(op.f('ix_accounts_user_id'), 'accounts', ['user_id'], unique=False)
    op.create_table('transactions',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('message', sa.String(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('receiver_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['receiver_id'], ['accounts.id'], ),
    sa.ForeignKeyConstraint(['sender_id'], ['accounts.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_receiver_id'), 'transactions', ['receiver_id'], unique=False)
    op.create_index(op.f('ix_transactions_sender_id'), 'transactions', ['sender_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_transactions_sender_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_receiver_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_accounts_user_id'), table_name='accounts')
    op.drop_index(op.f('ix_accounts_id'), table_name='accounts')
    op.drop_table('accounts')
    # ### end Alembic commands ###
