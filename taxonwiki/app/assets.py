# -*- coding: utf-8 -*-

from flask.ext.bootstrap import Bootstrap
from flask.ext.assets import Environment, Bundle


def init_app(app):
    Bootstrap(app)
    assets = Environment(app)
    app.assets = assets

    # main.js
    main_js = Bundle('javascripts/main.js',
                     filters='uglifyjs', output='gen/main.js')

    # main.css
    main_css = Bundle('stylesheets/main.scss',
                      filters='compass', output='gen/main.css')

    assets.register('main_js', main_js)
    assets.register('main_css', main_css)

    return assets
