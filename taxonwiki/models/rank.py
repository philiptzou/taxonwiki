# -*- coding: utf-8 -*-

from flask import current_app as app
from ._common import ENUM_ORGANISM

db = app.db


class Rank(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    name = db.Column(db.Unicode(1024), nullable=False)

    organism = db.Column(ENUM_ORGANISM)
