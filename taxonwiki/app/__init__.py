# -*- coding: utf-8 -*-

from flask import Flask
from . import db, assets, alembic


def init_app(env):
    assert env in ('development', 'testing', 'production')
    app = Flask('taxonwiki')
    app.config.from_object('taxonwiki.config.{0}Config'
                           .format(env.capitalize()))
    db.init_app(app)
    assets.init_app(app)
    alembic.init_app(app)
    return app
