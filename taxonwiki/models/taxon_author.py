# -*- coding: utf-8 -*-

from flask import current_app as app

db = app.db

ENUM_ANOTHER_TAXA_TYPE = db.Enum('parent', 'sibling',
                                 name='another_taxon_type_enum')


class TaxonAuthor(db.Model):

    __table_args__ = (db.UniqueConstraint('taxon_id', 'author_id'), )

    id = db.Column(db.BigInteger(), primary_key=True, nullable=False)

    taxon_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'),
                         nullable=False, index=True)

    author_id = db.Column(db.Integer(), db.ForeignKey('author.id'),
                          nullable=False, index=True)

    year = db.Column(db.Integer())
