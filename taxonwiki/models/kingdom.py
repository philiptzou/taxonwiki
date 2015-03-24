# -*- coding: utf-8 -*-

from flask import current_app as app

db = app.db


class Kingdom(db.Model):
    name = db.Column(db.Unicode(256), primary_key=True, nullable=False)
