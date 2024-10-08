"""empty message

Revision ID: 36c27d13e675
Revises: abe5b2d5e99b
Create Date: 2024-01-27 17:05:53.878249

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '36c27d13e675'
down_revision = 'abe5b2d5e99b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('server',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=False),
                    sa.Column('location', sa.String(length=100), nullable=False),
                    sa.Column('cpu', sa.Integer(), nullable=True),
                    sa.Column('ram', sa.Integer(), nullable=True),
                    sa.Column('ssd', sa.Integer(), nullable=True),
                    sa.Column('info_url', sa.String(length=255), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('deadline', sa.DateTime(), nullable=True),
                    sa.Column('online', sa.Boolean(), nullable=True),
                    sa.Column('owner_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['owner_id'], ['site_user.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('server')
    # ### end Alembic commands ###
