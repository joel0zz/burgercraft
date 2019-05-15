"""empty message

Revision ID: c56e118effb8
Revises: 342851cd6977
Create Date: 2019-03-09 15:30:36.132602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c56e118effb8'
down_revision = '342851cd6977'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image', sa.String(length=36), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'image')
    # ### end Alembic commands ###