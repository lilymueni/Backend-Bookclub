"""empty message

Revision ID: 224c36875099
Revises: 754ccb70d5ff
Create Date: 2024-07-14 15:10:02.937373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '224c36875099'
down_revision = '754ccb70d5ff'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('membership',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('book_club_id', sa.Integer(), nullable=True),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['book_club_id'], ['book_club.id'], name=op.f('fk_membership_book_club_id_book_club')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_membership_user_id_user')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('membership')
    # ### end Alembic commands ###
