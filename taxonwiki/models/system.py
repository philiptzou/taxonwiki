# -*- coding: utf-8 -*-

from flask import current_app as app
from sqlalchemy_utils import ArrowType, ChoiceType

from ._types import ORGANISM_TYPE

db = app.db


class System(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    name = db.Column(db.Unicode(1024), nullable=False)

    organism = db.Column(ChoiceType(ORGANISM_TYPE), nullable=False)

    published_at = db.Column(ArrowType(), nullable=False)
