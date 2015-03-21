"""Create taxon tables

Revision ID: 50cf10edc277
Revises:
Create Date: 2015-03-21 02:11:44.628045

"""

# revision identifiers, used by Alembic.
revision = '50cf10edc277'
down_revision = None
branch_labels = ()
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


def upgrade():
    op.create_table(
        'system',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(length=1024), nullable=False),
        sa.Column('organism',
                  sa.Enum('animal', 'bacterial', 'fungi', 'plant',
                          'protist', 'virus', name='organism_enum'),
                  nullable=False),
        sa.Column('published_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'rank',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.Unicode(length=1024), nullable=False),
        sa.Column('organism',
                  sa.Enum('animal', 'bacterial', 'fungi', 'plant',
                          'protist', 'virus', name='organism_enum'),
                  nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'taxon',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('scientific_name', sa.Unicode(length=1024), nullable=False),
        sa.Column('rank_id', sa.Integer(), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('authority', sa.Unicode(length=1024), nullable=True),
        sa.Column('organism',
                  sa.Enum('animal', 'bacterial', 'fungi', 'plant',
                          'protist', 'virus', name='organism_enum'),
                  nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['taxon.id'], ),
        sa.ForeignKeyConstraint(['rank_id'], ['rank.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('scientific_name')
    )
    op.create_index(op.f('ix_taxon_created_at'), 'taxon',
                    ['created_at'], unique=False)
    op.create_index(op.f('ix_taxon_parent_id'), 'taxon',
                    ['parent_id'], unique=False)
    op.create_index(op.f('ix_taxon_rank_id'), 'taxon',
                    ['rank_id'], unique=False)
    op.create_table(
        'taxon_alias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('taxon_id', sa.Integer(), nullable=False),
        sa.Column('another_taxon_type',
                  sa.Enum('en', 'zh-cn', 'zh-tw', 'zh-hk',
                          name='taxon_alias_language_enum'), nullable=True),
        sa.Column('is_primary', sa.Boolean(), nullable=False),
        sa.Column('name', sa.Unicode(length=1024), nullable=False),
        sa.ForeignKeyConstraint(['taxon_id'], ['taxon.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('taxon_id', 'is_primary')
    )
    op.create_index(op.f('ix_taxon_alias_name'), 'taxon_alias',
                    ['name'], unique=False)
    op.create_index(op.f('ix_taxon_alias_taxon_id'), 'taxon_alias',
                    ['taxon_id'], unique=False)
    op.create_table(
        'taxon_system',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('taxon_id', sa.Integer(), nullable=False),
        sa.Column('system_id', sa.Integer(), nullable=False),
        sa.Column('another_taxon_id', sa.Integer(), nullable=True),
        sa.Column('another_taxon_type',
                  sa.Enum('parent', 'sibling',
                          name='another_taxon_type_enum'),
                  nullable=True),
        sa.Column('is_recognized', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ['another_taxon_id'], ['taxon.id'], ),
        sa.ForeignKeyConstraint(['system_id'], ['system.id'], ),
        sa.ForeignKeyConstraint(['taxon_id'], ['taxon.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_taxon_system_another_taxon_id'),
                    'taxon_system', ['another_taxon_id'], unique=False)
    op.create_index(op.f('ix_taxon_system_system_id'), 'taxon_system',
                    ['system_id'], unique=False)
    op.create_index(op.f('ix_taxon_system_taxon_id'), 'taxon_system',
                    ['taxon_id'], unique=False)
    op.create_table(
        'taxon_revision',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('taxon_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.UnicodeText(), nullable=True),
        sa.Column(
            'comment', sa.Unicode(length=1024), nullable=True),
        sa.Column(
            'created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['taxon_id'], ['taxon.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_taxon_revision_taxon_id'), 'taxon_revision',
                    ['taxon_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_taxon_revision_taxon_id'), table_name='taxon_revision')
    op.drop_table('taxon_revision')
    op.drop_index(op.f('ix_taxon_system_taxon_id'), table_name='taxon_system')
    op.drop_index(op.f('ix_taxon_system_system_id'), table_name='taxon_system')
    op.drop_index(
        op.f('ix_taxon_system_another_taxon_id'), table_name='taxon_system')
    op.drop_table('taxon_system')
    op.drop_index(op.f('ix_taxon_alias_taxon_id'), table_name='taxon_alias')
    op.drop_index(op.f('ix_taxon_alias_name'), table_name='taxon_alias')
    op.drop_table('taxon_alias')
    op.drop_index(op.f('ix_taxon_rank_id'), table_name='taxon')
    op.drop_index(op.f('ix_taxon_parent_id'), table_name='taxon')
    op.drop_index(op.f('ix_taxon_created_at'), table_name='taxon')
    op.drop_table('taxon')
    op.drop_table('rank')
    op.drop_table('system')
    ENUM(name='another_taxon_type_enum').drop(op.get_bind(), checkfirst=False)
    ENUM(name='organism_enum').drop(op.get_bind(), checkfirst=False)
    ENUM(name='taxon_alias_language_enum').drop(op.get_bind(), checkfirst=False)
