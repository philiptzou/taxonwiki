# -*- coding: utf-8 -*-

from flask import current_app as app
from sqlalchemy_utils import TSVectorType

db = app.db


class Author(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    name = db.Column(db.Unicode(1024), nullable=False, unique=True)

    name_vector = db.Column(TSVectorType('name'))
