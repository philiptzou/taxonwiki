# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms_alchemy import model_form_factory

BaseModelForm = model_form_factory(Form)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return current_app.db.session


def init_app(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']
    db = SQLAlchemy(app)
    app.db = db
    app.ModelForm = ModelForm
    with app.app_context():
        from .. import models
        app.models = models
    return db
