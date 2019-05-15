"""empty message

Revision ID: e3e3108c97c7
Revises: 54a41b8b78a2
Create Date: 2019-04-07 14:23:23.026111

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3e3108c97c7'
down_revision = '54a41b8b78a2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comment', sa.Column('comment_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comment', 'comment_date')
    # ### end Alembic commands ###