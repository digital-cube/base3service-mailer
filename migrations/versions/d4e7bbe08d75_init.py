"""init

Revision ID: d4e7bbe08d75
Revises: 
Create Date: 2020-11-13 19:06:31.736703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd4e7bbe08d75'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mails',
    sa.Column('id', postgresql.UUID(), nullable=False),
    sa.Column('created', sa.TIMESTAMP(), nullable=True),
    sa.Column('id_user', postgresql.UUID(), nullable=False),
    sa.Column('sender_name', sa.String(), nullable=True),
    sa.Column('sender_email', sa.String(), nullable=False),
    sa.Column('receiver_name', sa.String(), nullable=True),
    sa.Column('receiver_email', sa.String(), nullable=False),
    sa.Column('subject', sa.String(), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('response_status', sa.String(), nullable=True),
    sa.Column('sent_timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mails_created'), 'mails', ['created'], unique=False)
    op.create_index(op.f('ix_mails_id_user'), 'mails', ['id_user'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_mails_id_user'), table_name='mails')
    op.drop_index(op.f('ix_mails_created'), table_name='mails')
    op.drop_table('mails')
    # ### end Alembic commands ###
