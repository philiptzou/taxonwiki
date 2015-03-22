# -*- coding: utf-8 -*-

from flask import Flask
from .app import db, assets, alembic


def init_app(env):
    assert env in ('development', 'testing', 'production')
    app = Flask(__name__)
    app.config.from_object('taxonwiki.config.{0}Config'
                           .format(env.capitalize()))
    db.init_app(app)
    assets.init_app(app)
    alembic.init_app(app)

    with app.app_context():
        from . import views  # noqa

    return app
