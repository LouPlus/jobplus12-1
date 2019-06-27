"""add user table enable field

Revision ID: e180c660abfb
Revises: eb3881665de3
Create Date: 2019-06-26 13:04:32.863761

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e180c660abfb'
down_revision = 'eb3881665de3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('enable', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'enable')
    # ### end Alembic commands ###