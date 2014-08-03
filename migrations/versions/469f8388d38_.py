"""Initial state

Revision ID: 469f8388d38
Revises: None
Create Date: 2014-08-03 13:13:00.234256

"""

# revision identifiers, used by Alembic.
revision = '469f8388d38'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=True),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('group',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sortcode', sa.String(length=10), nullable=False),
        sa.Column('slug', sa.String(length=10), nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('code'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('slug'),
        sa.UniqueConstraint('sortcode')
    )
    op.create_table('event',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('sort_date', sa.Date(), nullable=True),
        sa.Column('dateline', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('guardian',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=15), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('confirmed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    op.create_table('korist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.Column('first_name', sa.String(length=100), nullable=False),
        sa.Column('last_name', sa.String(length=100), nullable=False),
        sa.Column('address1', sa.Text(), nullable=False),
        sa.Column('address2', sa.Text(), nullable=True),
        sa.Column('phone', sa.String(length=15), nullable=False),
        sa.Column('mobile', sa.String(length=15), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('birthday', sa.Date(), nullable=False),
        sa.Column('allergies', sa.Text(), nullable=True),
        sa.Column('other_info', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['group_id'], ['group.id']),
        sa.ForeignKeyConstraint(['profile_id'], ['profile.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event__group',
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('group_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
        sa.ForeignKeyConstraint(['group_id'], ['group.id'])
    )
    op.create_table('OSA',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('osa', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('event_id', sa.Integer(), nullable=True),
        sa.Column('korist_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['event.id']),
        sa.ForeignKeyConstraint(['korist_id'], ['korist.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role__user',
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['role_id'], ['role.id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'])
    )
    op.create_table('korist__guardian',
        sa.Column('korist_id', sa.Integer(), nullable=True),
        sa.Column('guardian_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['guardian_id'], ['guardian.id']),
        sa.ForeignKeyConstraint(['korist_id'], ['korist.id'])
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('korist__guardian')
    op.drop_table('role__user')
    op.drop_table('OSA')
    op.drop_table('event__group')
    op.drop_table('korist')
    op.drop_table('user')
    op.drop_table('guardian')
    op.drop_table('event')
    op.drop_table('group')
    op.drop_table('role')
    op.drop_table('profile')
    ### end Alembic commands ###
