# -*- coding: utf-8 -*-

from flask import (request,
                   render_template,
                   current_app as app)


@app.route('/')
def home():
    assert request
    return render_template('home.html')
