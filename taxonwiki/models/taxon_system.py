# -*- coding: utf-8 -*-

from flask import current_app as app

db = app.db

ENUM_ANOTHER_TAXA_TYPE = db.Enum('parent', 'sibling',
                                 name='another_taxon_type_enum')


class TaxonSystem(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    taxon_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'),
                        nullable=False, index=True)

    system_id = db.Column(db.Integer(), db.ForeignKey('system.id'),
                          nullable=False, index=True)

    another_taxon_id = db.Column(db.Integer(),
                                db.ForeignKey('taxon.id'), index=True)

    another_taxon_type = db.Column(ENUM_ANOTHER_TAXA_TYPE)

    is_recognized = db.Column(db.Boolean(), nullable=False)
