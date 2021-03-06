"""empty message

Revision ID: 260505d337d3
Revises: feb15b4e44e5
Create Date: 2021-11-08 19:21:07.348030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '260505d337d3'
down_revision = 'feb15b4e44e5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('user_country')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_country', sa.VARCHAR(length=3), nullable=True))

    # ### end Alembic commands ###
