"""update job table and seeker_job table

Revision ID: 3867a39b4bef
Revises: e180c660abfb
Create Date: 2019-06-27 16:30:11.533708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3867a39b4bef'
down_revision = 'e180c660abfb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('online', sa.Boolean(), nullable=True))
    op.create_index(op.f('ix_job_online'), 'job', ['online'], unique=False)
    op.add_column('seeker_job', sa.Column('freed_back', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('seeker_job', 'freed_back')
    op.drop_index(op.f('ix_job_online'), table_name='job')
    op.drop_column('job', 'online')
    # ### end Alembic commands ###