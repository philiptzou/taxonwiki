# -*- coding: utf-8 -*-

from flask import current_app as app

db = app.db

ENUM_LANGUAGE = db.Enum('en', 'zh-cn', 'zh-tw', 'zh-hk',
                        name='taxon_alias_language_enum')


class TaxonAlias(db.Model):

    __table_args__ = (db.UniqueConstraint('taxon_id', 'is_primary'),)

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    taxon_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'),
                        nullable=False, index=True)

    another_taxon_type = db.Column(ENUM_LANGUAGE)

    is_primary = db.Column(db.Boolean(), nullable=False)

    name = db.Column(db.Unicode(1024), index=True, nullable=False)
