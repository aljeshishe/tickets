"""added airport info

Revision ID: 67df0b232815
Revises: 4d1134731c04
Create Date: 2019-03-12 22:00:52.043870

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '67df0b232815'
down_revision = '4d1134731c04'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('airport', sa.Column('city_name', sa.String(length=50), nullable=True))
    op.add_column('airport', sa.Column('country', sa.String(length=50), nullable=True))
    op.add_column('airport', sa.Column('country_code', sa.String(length=5), nullable=True))
    op.add_column('airport', sa.Column('latitude', sa.Float(), nullable=True))
    op.add_column('airport', sa.Column('longitude', sa.Float(), nullable=True))
    op.drop_column('airport', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('airport', sa.Column('name', mysql.VARCHAR(length=32), nullable=True))
    op.drop_column('airport', 'longitude')
    op.drop_column('airport', 'latitude')
    op.drop_column('airport', 'country_code')
    op.drop_column('airport', 'country')
    op.drop_column('airport', 'city_name')
    # ### end Alembic commands ###
