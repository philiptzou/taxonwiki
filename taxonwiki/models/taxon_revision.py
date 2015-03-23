# -*- coding: utf-8 -*-

from flask import current_app as app
from sqlalchemy_utils import ArrowType

db = app.db


class TaxonRevision(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    taxon_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'),
                         nullable=False, index=True)

    # TODO: use PostgreSQL jsonb
    body = db.Column(db.UnicodeText())

    comment = db.Column(db.Unicode(1024))

    created_at = db.Column(ArrowType(), nullable=False)
