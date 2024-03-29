"""empty message

Revision ID: 9ba880a6d240
Revises: 60e8cdd90b57
Create Date: 2023-02-17 19:53:26.881158

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9ba880a6d240'
down_revision = '60e8cdd90b57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog__user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('signature', sa.String(length=100), nullable=True))
        batch_op.drop_column('hobby')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blog__user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hobby', mysql.VARCHAR(length=100), nullable=True))
        batch_op.drop_column('signature')

    # ### end Alembic commands ###
