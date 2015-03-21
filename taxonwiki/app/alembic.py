# -*- coding: utf-8 -*-

from flask.ext.alembic import Alembic


def init_app(app):
    alembic = Alembic(app)
    app.alembic = alembic
    return alembic
