# -*- coding: utf-8 -*-

import arrow

from wtforms import fields
from flask import current_app as app, abort, url_for
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import ChoiceType, ArrowType

from ._types import ORGANISM_TYPE, RANK_TYPE
from ..lib import orm_helpers

db = app.db


class Taxon(db.Model):

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    scientific_name = db.Column(db.Unicode(1024),
                                unique=True, nullable=False,
                                info={'label': 'Scientific name'})

    rank = db.Column(ChoiceType(RANK_TYPE),
                     nullable=False, index=True,
                     info={'label': 'Rank'})

    parent_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'), index=True)

    authority = db.Column(db.Unicode(1024),
                          info={'label': 'Authority'})

    organism = db.Column(ChoiceType(ORGANISM_TYPE), nullable=False,
                         info={'label': 'Organism'})

    created_at = db.Column(ArrowType(),
                           nullable=False, index=True)

    updated_at = db.Column(ArrowType())

    def __init__(self, scientific_name=None, **args):
        self._form = None
        super(Taxon, self).__init__(
            scientific_name=scientific_name, **args)

    def url(self, method='show', **args):
        if method in ('index', 'new'):
            url = url_for('TaxonView:{0}'.format(method), **args)
        else:
            url = url_for('TaxonView:{0}'.format(method),
                          scientific_name=self.scientific_name,
                          **args)
        return url

    @property
    def form(self):
        return self._form

    @classmethod
    def is_exists(cls, scientific_name):
        exists = cls.query.filter_by(scientific_name=scientific_name).count()
        return bool(exists)

    @classmethod
    def create(cls, unsafe_form):
        self = cls()
        success = False
        if cls.is_exists(unsafe_form.get('scientific_name')):
            abort(409)
        self._form = safe_form = TaxonForm(unsafe_form)
        if safe_form.validate_on_submit():
            safe_form.populate_obj(self)
            self.created_at = arrow.now()
            db.session.add(self)
            success = True
        return self, success

    @classmethod
    def retrieve(cls, scientific_name):
        try:
            self = cls.query.filter_by(scientific_name=scientific_name).one()
        except NoResultFound:
            abort(404, 'The requested taxon was not found.')
        return self

    def update(self, unsafe_form):
        self._form = safe_form = TaxonForm(unsafe_form, obj=self)
        success = False
        if safe_form.validate_on_submit():
            safe_form.populate_obj(self)
            # forbid to edit scientific name though update
            if orm_helpers.is_changed(self, 'scientific_name'):
                abort(403, 'Scientific name can not be changeed.')
            if orm_helpers.is_changed(self):
                self.updated_at = arrow.now()
            success = True
        return self, success

    def update_scientific_name(self, name):
        if not self.is_exists(name):
            self.scientific_name = name


class TaxonForm(app.ModelForm):

    class Meta:
        model = Taxon
        exclude = ['created_at', 'updated_at']
        strip_string_fields = True

TaxonForm.submit = fields.SubmitField('Submit')
