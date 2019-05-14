"""empty message

Revision ID: b1717af72fcf
Revises: 56459171a153
Create Date: 2019-04-07 09:58:24.387807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1717af72fcf'
down_revision = '56459171a153'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('comment_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'post', 'comment', ['comment_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'post', type_='foreignkey')
    op.drop_column('post', 'comment_id')
    # ### end Alembic commands ###
