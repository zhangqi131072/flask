"""empty message

Revision ID: b020bb0c466c
Revises: ea660549ea38
Create Date: 2017-12-18 17:19:00.137875

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b020bb0c466c'
down_revision = 'ea660549ea38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('albums_score', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('articles_score', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('comments_score', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('creator_score', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'creator_score')
    op.drop_column('user', 'comments_score')
    op.drop_column('user', 'articles_score')
    op.drop_column('user', 'albums_score')
    # ### end Alembic commands ###