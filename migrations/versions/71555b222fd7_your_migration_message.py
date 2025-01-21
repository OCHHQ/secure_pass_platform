"""Your migration message

Revision ID: 71555b222fd7
Revises: f2040fdbcc2d
Create Date: 2025-01-04 11:46:01.958457

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71555b222fd7'
down_revision = 'f2040fdbcc2d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shared_password', schema=None) as batch_op:
        batch_op.add_column(sa.Column('token', sa.String(length=200), nullable=False))
        batch_op.add_column(sa.Column('expiry_time', sa.DateTime(), nullable=False))
        batch_op.add_column(sa.Column('is_used', sa.Boolean(), nullable=False))
        batch_op.create_unique_constraint('uq_shared_password_token', ['token'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shared_password', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('is_used')
        batch_op.drop_column('expiry_time')
        batch_op.drop_column('token')

    # ### end Alembic commands ###