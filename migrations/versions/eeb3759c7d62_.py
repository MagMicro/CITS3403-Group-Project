"""empty message

Revision ID: eeb3759c7d62
Revises: 111cbb522582
Create Date: 2024-04-26 22:07:32.130619

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eeb3759c7d62'
down_revision = '111cbb522582'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.DATETIME(),
               type_=sa.String(length=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Users', schema=None) as batch_op:
        batch_op.alter_column('date',
               existing_type=sa.String(length=10),
               type_=sa.DATETIME(),
               existing_nullable=True)

    # ### end Alembic commands ###
