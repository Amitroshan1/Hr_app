"""update leave model

Revision ID: a8bda0737dd2
Revises: 89f5127c1854
Create Date: 2024-09-17 12:20:16.095886

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a8bda0737dd2'
down_revision = '89f5127c1854'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leave_applications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leave_applications', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###