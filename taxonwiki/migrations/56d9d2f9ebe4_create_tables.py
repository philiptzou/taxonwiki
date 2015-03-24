"""Create tables

Revision ID: 56d9d2f9ebe4
Revises: 
Create Date: 2015-03-24 01:00:40.029527

"""

# revision identifiers, used by Alembic.
revision = '56d9d2f9ebe4'
down_revision = None
branch_labels = ()
depends_on = None

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils as su


def upgrade():
    op.create_table('kingdom',
                    sa.Column('name', sa.Unicode(length=256), nullable=False),
                    sa.PrimaryKeyConstraint('name')
                    )
    op.create_table('author',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Unicode(length=1024), nullable=False),
                    sa.Column(
                        'name_vector', su.TSVectorType(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('rank',
                    sa.Column('name', sa.Unicode(length=256), nullable=False),
                    sa.Column(
                        'kingdom_name', sa.Unicode(length=256), nullable=False),
                    sa.Column(
                        'direct_parent_rank_name', sa.Unicode(length=256), nullable=True),
                    sa.Column('required_parent_rank_name', sa.Unicode(
                        length=256), nullable=True),
                    sa.Column('ordinal', sa.SmallInteger(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['direct_parent_rank_name', 'kingdom_name'], ['rank.name', 'rank.kingdom_name'], ),
                    sa.ForeignKeyConstraint(
                        ['kingdom_name'], ['kingdom.name'], ),
                    sa.ForeignKeyConstraint(
                        ['required_parent_rank_name', 'kingdom_name'], ['rank.name', 'rank.kingdom_name'], ),
                    sa.PrimaryKeyConstraint('name', 'kingdom_name'),
                    )
    op.create_index(op.f('ix_rank_direct_parent_rank_name'),
                    'rank', ['direct_parent_rank_name'], unique=False)
    op.create_index(op.f('ix_rank_required_parent_rank_name'),
                    'rank', ['required_parent_rank_name'], unique=False)
    op.create_index(op.f('ix_rank_ordinal'),
                    'rank', ['ordinal'], unique=False)
    op.create_table('taxon',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column(
                        'scientific_name', sa.Unicode(length=1024), nullable=False),
                    sa.Column(
                        'status', sa.Unicode(length=255), nullable=False),
                    sa.Column(
                        'invalid_reason', sa.Unicode(length=256), nullable=True),
                    sa.Column('itis_tsn', sa.Integer(), nullable=True),
                    sa.Column('parent_id', sa.Integer(), nullable=True),
                    sa.Column('rank_name', sa.Unicode(), nullable=False),
                    sa.Column(
                        'kingdom_name', sa.Unicode(length=256), nullable=True),
                    sa.Column(
                        'author_abbr', sa.Unicode(length=1024), nullable=True),
                    sa.Column(
                        'created_at', su.ArrowType(), nullable=False),
                    sa.Column(
                        'updated_at', su.ArrowType(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['kingdom_name'], ['kingdom.name'], ),
                    sa.ForeignKeyConstraint(['parent_id'], ['taxon.id'], ),
                    sa.ForeignKeyConstraint(
                        ['rank_name', 'kingdom_name'], ['rank.name', 'rank.kingdom_name'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('scientific_name', 'rank_name', 'kingdom_name')
                    )
    op.create_index(
        op.f('ix_taxon_itis_tsn'), 'taxon', ['itis_tsn'], unique=False)
    op.create_index(
        op.f('ix_taxon_created_at'), 'taxon', ['created_at'], unique=False)
    op.create_index(
        op.f('ix_taxon_kingdom_name'), 'taxon', ['kingdom_name'], unique=False)
    op.create_index(
        op.f('ix_taxon_parent_id'), 'taxon', ['parent_id'], unique=False)
    op.create_index(
        op.f('ix_taxon_rank_name'), 'taxon', ['rank_name'], unique=False)
    op.create_index('ix_taxon_rank_name_rank_kingdom_name', 'taxon', [
                    'rank_name', 'kingdom_name'], unique=False)
    op.create_table('taxon_revision',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('taxon_id', sa.Integer(), nullable=False),
                    sa.Column('body', sa.UnicodeText(), nullable=True),
                    sa.Column(
                        'comment', sa.Unicode(length=1024), nullable=True),
                    sa.Column(
                        'created_at', su.ArrowType(), nullable=False),
                    sa.ForeignKeyConstraint(['taxon_id'], ['taxon.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_taxon_revision_taxon_id'),
                    'taxon_revision', ['taxon_id'], unique=False)
    op.create_table('taxon_author',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('taxon_id', sa.Integer(), nullable=False),
                    sa.Column('author_id', sa.Integer(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['author_id'], ['author.id'], ),
                    sa.ForeignKeyConstraint(['taxon_id'], ['taxon.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('taxon_id', 'author_id')
                    )
    op.create_index(
        op.f('ix_taxon_author_author_id'), 'taxon_author', ['author_id'], unique=False)
    op.create_index(
        op.f('ix_taxon_author_taxon_id'), 'taxon_author', ['taxon_id'], unique=False)
    op.create_table('taxon_alias',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('taxon_id', sa.Integer(), nullable=False),
                    sa.Column(
                        'language', sa.Unicode(length=255), nullable=True),
                    sa.Column('is_primary', sa.Boolean(), nullable=False),
                    sa.Column('name', sa.Unicode(length=1024), nullable=False),
                    sa.ForeignKeyConstraint(['taxon_id'], ['taxon.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('taxon_id', 'is_primary')
                    )
    op.create_index(
        op.f('ix_taxon_alias_name'), 'taxon_alias', ['name'], unique=False)
    op.create_index(
        op.f('ix_taxon_alias_taxon_id'), 'taxon_alias', ['taxon_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_taxon_alias_taxon_id'), table_name='taxon_alias')
    op.drop_index(op.f('ix_taxon_alias_name'), table_name='taxon_alias')
    op.drop_table('taxon_alias')
    op.drop_index(op.f('ix_taxon_author_taxon_id'), table_name='taxon_author')
    op.drop_index(op.f('ix_taxon_author_author_id'), table_name='taxon_author')
    op.drop_table('taxon_author')
    op.drop_index(
        op.f('ix_taxon_revision_taxon_id'), table_name='taxon_revision')
    op.drop_table('taxon_revision')
    op.drop_index('ix_taxon_rank_name_rank_kingdom_name', table_name='taxon')
    op.drop_index(op.f('ix_taxon_rank_name'), table_name='taxon')
    op.drop_index(op.f('ix_taxon_parent_id'), table_name='taxon')
    op.drop_index(op.f('ix_taxon_kingdom_name'), table_name='taxon')
    op.drop_index(op.f('ix_taxon_created_at'), table_name='taxon')
    op.drop_index(op.f('ix_taxon_itis_tsn'), table_name='taxon')
    op.drop_table('taxon')
    op.drop_index(op.f('ix_rank_ordinal'), table_name='rank')
    op.drop_index(op.f('ix_rank_required_parent_rank_name'), table_name='rank')
    op.drop_index(op.f('ix_rank_direct_parent_rank_name'), table_name='rank')
    op.drop_table('rank')
    op.drop_table('author')
    op.drop_table('kingdom')
