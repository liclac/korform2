"""Non-nullable fields

Revision ID: 35c4ab1bfdda
Revises: 4f953349e0d
Create Date: 2015-07-12 13:56:15.891734

"""

# revision identifiers, used by Alembic.
revision = '35c4ab1bfdda'
down_revision = '4f953349e0d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('event', 'sort_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('korist', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    op.alter_column('korist', 'mobile',
               existing_type=sa.VARCHAR(length=15),
               nullable=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('korist', 'mobile',
               existing_type=sa.VARCHAR(length=15),
               nullable=True)
    op.alter_column('korist', 'email',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    op.alter_column('event', 'sort_date',
               existing_type=sa.DATE(),
               nullable=True)
    ### end Alembic commands ###