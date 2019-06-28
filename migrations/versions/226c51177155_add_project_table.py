"""add project table

Revision ID: 226c51177155
Revises: b9c0bb591693
Create Date: 2019-06-28 11:59:06.120045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '226c51177155'
down_revision = 'b9c0bb591693'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.Column('in_time', sa.DateTime(), nullable=False),
    sa.Column('out_time', sa.DateTime(), nullable=False),
    sa.Column('desc', sa.TEXT(), nullable=True),
    sa.Column('seeker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['seeker_id'], ['seeker.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('project')
    # ### end Alembic commands ###
