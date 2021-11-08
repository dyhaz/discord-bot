"""create coupon table

Revision ID: a308fc57244b
Revises: 
Create Date: 2021-11-08 09:37:21.744173

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = 'a308fc57244b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'coupon',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200)),
        sa.Column('url', sa.String(100)),
        sa.Column('voucher_id', sa.Integer),
        sa.Column('created_date', sa.DateTime, server_default=func.now(), onupdate=func.now()),
        sa.Column('is_deleted', sa.Boolean)
    )


def downgrade():
    op.drop_table('coupon')

