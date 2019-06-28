"""update seeker table

Revision ID: 15daee00a9ab
Revises: 0b8c43888e5d
Create Date: 2019-06-28 11:03:10.373029

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15daee00a9ab'
down_revision = '0b8c43888e5d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seeker', 'education')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('seeker', sa.Column('education', mysql.VARCHAR(length=12), nullable=True))
    # ### end Alembic commands ###
