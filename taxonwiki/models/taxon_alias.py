# -*- coding: utf-8 -*-

from flask import current_app as app
from sqlalchemy_utils import ChoiceType

from ._types import LANGUAGE_TYPE

db = app.db


class TaxonAlias(db.Model):

    __table_args__ = (db.UniqueConstraint('taxon_id', 'is_primary'),)

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    taxon_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'),
                         nullable=False, index=True)

    language = db.Column(ChoiceType(LANGUAGE_TYPE))

    is_primary = db.Column(db.Boolean(), nullable=False)

    name = db.Column(db.Unicode(1024), index=True, nullable=False)
