"""empty message

Revision ID: 82c4b727f94f
Revises: 3bdbe844e71e
Create Date: 2017-12-17 14:36:00.918300

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '82c4b727f94f'
down_revision = '3bdbe844e71e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_follow')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_follow',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('followed_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('follower_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True),
    sa.Column('addtime', mysql.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], name='user_follow_ibfk_1'),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], name='user_follow_ibfk_2'),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
