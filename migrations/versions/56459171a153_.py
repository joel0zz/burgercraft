"""empty message

Revision ID: 56459171a153
Revises: 892717a4c638
Create Date: 2019-03-20 22:48:04.979839

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56459171a153'
down_revision = '892717a4c638'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('comment', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    # ### end Alembic commands ###
