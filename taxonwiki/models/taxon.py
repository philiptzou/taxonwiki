# -*- coding: utf-8 -*-

from datetime import datetime
from flask import current_app as app
from ._common import ENUM_ORGANISM

db = app.db


class Taxon(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    scientific_name = db.Column(db.Unicode(1024),
                                unique=True, nullable=False)

    rank_id = db.Column(db.Integer(), db.ForeignKey('rank.id'),
                        nullable=False, index=True)

    parent_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'), index=True)

    authority = db.Column(db.Unicode(1024))

    organism = db.Column(ENUM_ORGANISM, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True),
                           nullable=False, index=True)

    updated_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, scientific_name, rank_id,
                 parent_id, authority, organism):
        self.scientific_name = scientific_name
        self.__update(rank_id, parent_id, authority, organism)
        self.created_at = datetime.now()

    @classmethod
    def create(cls, scientific_name, rank_id,
               parent_id, authority, organism):
        self = cls(scientific_name, rank_id, parent_id, authority, organism)
        db.session.add(self)

    def __update(self, rank_id, parent_id, authority, organism):
        self.rank_id = rank_id
        self.parent_id = parent_id
        self.authority = authority
        self.organism = organism

    def update(self, rank_id, parent_id, authority, organism):
        self.__update(rank_id, parent_id, authority, organism)
        self.updated_at = datetime.now()

    def scientific_name_exists(self, scientific_name):
        exists = Taxon.query.filter_by(scientific_name=scientific_name).count()
        return bool(exists)

    def update_scientific_name(self, name):
        if not self.scientific_name_exists(name):
            self.scientific_name = name
