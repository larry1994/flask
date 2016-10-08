"""empty message

Revision ID: 185a694c8e
Revises: 2e8db23de26
Create Date: 2016-04-27 18:27:51.605660

"""

# revision identifiers, used by Alembic.
revision = '185a694c8e'
down_revision = '2e8db23de26'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('time', sa.String(length=50), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'time')
    ### end Alembic commands ###