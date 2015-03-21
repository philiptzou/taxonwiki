# -*- coding: utf-8 -*-

from flask.ext.assets import Environment


def init_app(app):
    assets = Environment(app)
    return assets
