"""empty message

Revision ID: 61e0a5c1a64c
Revises: 
Create Date: 2023-01-24 23:11:26.100009

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61e0a5c1a64c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('nombre', sa.String(length=20), nullable=False),
    sa.Column('apellido', sa.String(length=20), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('actividades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tiempo', sa.String(length=100), nullable=False),
    sa.Column('distancia', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.Column('emocion', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tiempo')
    )
    op.create_table('recetas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('receta', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['email'], ['user.email'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('receta')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recetas')
    op.drop_table('actividades')
    op.drop_table('user')
    # ### end Alembic commands ###
