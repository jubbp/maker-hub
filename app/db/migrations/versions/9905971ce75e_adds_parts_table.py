"""Adds Parts Table

Revision ID: 9905971ce75e
Revises: 
Create Date: 2021-05-30 13:36:19.477030

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9905971ce75e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('part',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('footprint', sa.String(), nullable=True),
    sa.Column('manufacturer', sa.String(), nullable=True),
    sa.Column('mpn', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_part_created_at'), 'part', ['created_at'], unique=False)
    op.create_index(op.f('ix_part_description'), 'part', ['description'], unique=False)
    op.create_index(op.f('ix_part_footprint'), 'part', ['footprint'], unique=False)
    op.create_index(op.f('ix_part_manufacturer'), 'part', ['manufacturer'], unique=False)
    op.create_index(op.f('ix_part_mpn'), 'part', ['mpn'], unique=False)
    op.create_index(op.f('ix_part_name'), 'part', ['name'], unique=False)
    op.create_index(op.f('ix_part_updated_at'), 'part', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_part_updated_at'), table_name='part')
    op.drop_index(op.f('ix_part_name'), table_name='part')
    op.drop_index(op.f('ix_part_mpn'), table_name='part')
    op.drop_index(op.f('ix_part_manufacturer'), table_name='part')
    op.drop_index(op.f('ix_part_footprint'), table_name='part')
    op.drop_index(op.f('ix_part_description'), table_name='part')
    op.drop_index(op.f('ix_part_created_at'), table_name='part')
    op.drop_table('part')
    # ### end Alembic commands ###
