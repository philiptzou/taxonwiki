# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
    db = SQLAlchemy(app)
    app.db = db
    with app.app_context():
        from .. import models
        app.models = models
    return db
