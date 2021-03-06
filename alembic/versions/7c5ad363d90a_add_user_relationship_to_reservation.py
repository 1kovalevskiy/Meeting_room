"""Add user relationship to Reservation

Revision ID: 7c5ad363d90a
Revises: af6e7fbe82dd
Create Date: 2022-05-29 20:32:51.154352

"""
import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c5ad363d90a'
down_revision = 'af6e7fbe82dd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', fastapi_users_db_sqlalchemy.guid.GUID(), nullable=True))
        batch_op.create_foreign_key('fk_reservation_user_id_user', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_constraint('fk_reservation_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
