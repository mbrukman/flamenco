"""uuid for managers

Revision ID: 28015a6e5b8
Revises: 4e25f581d8bd
Create Date: 2015-01-21 11:27:14.871890

"""

# revision identifiers, used by Alembic.
revision = '28015a6e5b8'
down_revision = '4e25f581d8bd'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manager', schema=None) as batch_op:
        batch_op.add_column(sa.Column('uuid', sa.String(length=128), nullable=True, unique=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('manager', schema=None) as batch_op:
        batch_op.drop_column('uuid')

    ### end Alembic commands ###
