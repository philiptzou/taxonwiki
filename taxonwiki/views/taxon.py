# -*- coding: utf-8 -*-

from flask import (request, redirect,
                   render_template,
                   current_app as app)
from flask.ext.classy import FlaskView, route


class TaxonView(FlaskView):

    @staticmethod
    def _get_model():
        return app.models.Taxon

    @route('/<scientific_name>/')
    def show(self, scientific_name):
        taxon = self._get_model().retrieve(scientific_name)
        return render_template('taxon/view.html', taxon=taxon)

    @route('/new/', methods=['GET', 'POST'])
    def new(self):
        taxon, success = self._get_model().create(request.form)
        if success:
            app.db.session.commit()
            return redirect(taxon.url())
        return render_template('taxon/edit.html',
                               taxon=taxon, is_creating=True)

    @route('/<scientific_name>/edit/', methods=['GET', 'POST'])
    def edit(self, scientific_name):
        taxon = self._get_model().retrieve(scientific_name)
        taxon, success = taxon.update(request.form)
        if success:
            app.db.session.commit()
            return redirect(taxon.url())
        return render_template('taxon/edit.html',
                               taxon=taxon, is_creating=False)

TaxonView.register(app)
