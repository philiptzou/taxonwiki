# -*- coding: utf-8 -*-

from flask import current_app as app

db = app.db


class Rank(db.Model):

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['direct_parent_rank_name', 'kingdom_name'],
            ['rank.name', 'rank.kingdom_name']
        ),
        db.ForeignKeyConstraint(
            ['required_parent_rank_name', 'kingdom_name'],
            ['rank.name', 'rank.kingdom_name']
        ))

    name = db.Column(db.Unicode(256), primary_key=True, nullable=False)

    kingdom_name = db.Column(db.Unicode(256),
                             db.ForeignKey('kingdom.name'),
                             primary_key=True, nullable=False)

    direct_parent_rank_name = db.Column(db.Unicode(256), index=True)

    required_parent_rank_name = db.Column(db.Unicode(256), index=True)

    ordinal = db.Column(db.SmallInteger(), nullable=False, index=True)
