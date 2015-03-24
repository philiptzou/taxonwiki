# -*- coding: utf-8 -*-

import arrow

from wtforms import fields
from flask import current_app as app, abort, url_for
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils import ChoiceType, ArrowType

from ._types import TAXON_STATUS_TYPE
from ..lib import orm_helpers

db = app.db


class Taxon(db.Model):

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['rank_name', 'kingdom_name'],
            ['rank.name', 'rank.kingdom_name']),
        db.UniqueConstraint('scientific_name', 'rank_name', 'kingdom_name'),
        db.Index('ix_taxon_rank_name_rank_kingdom_name',
                 'rank_name', 'kingdom_name'))

    id = db.Column(db.Integer(), primary_key=True, nullable=False)

    scientific_name = db.Column(db.Unicode(1024),
                                nullable=False,
                                info={'label': 'Scientific name'})

    status = db.Column(ChoiceType(TAXON_STATUS_TYPE),
                       nullable=False, info={'label': 'Status'})

    invalid_reason = db.Column(db.Unicode(256),
                               info={'label': 'Invalid reason'})

    itis_tsn = db.Column(db.Integer(), index=True)

    parent_id = db.Column(db.Integer(), db.ForeignKey('taxon.id'), index=True)

    rank_name = db.Column(db.Unicode(), nullable=False, index=True)

    kingdom_name = db.Column(db.Unicode(256),
                             db.ForeignKey('kingdom.name'), index=True)

    author_abbr = db.Column(db.Unicode(1024),
                            info={'label': 'Author (abbreviate)'})

    created_at = db.Column(ArrowType(),
                           nullable=False, index=True)

    updated_at = db.Column(ArrowType())

    def __init__(self, scientific_name=None, **args):
        self._form = None
        super(Taxon, self).__init__(
            scientific_name=scientific_name, **args)

    def __repr__(self):
        return '<Taxon({0}, tsn={1}) object at {2}>'.format(
            repr(self.scientific_name), repr(self.itis_tsn),
            hex(id(self)))

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
    def is_exists(cls, scientific_name, rank_name, kingdom_name):
        exists = cls.query.filter_by(
            scientific_name=scientific_name,
            rank_name=rank_name, kingdom_name=kingdom_name
        ).count()
        return bool(exists)

    @classmethod
    def form_create(cls, unsafe_form):
        self = cls()
        success = False
        if cls.is_exists(
                unsafe_form.get('scientific_name'),
                unsafe_form.get('rank_name'),
                unsafe_form.get('kingdom_name')):
            abort(409)
        self._form = safe_form = TaxonForm(unsafe_form)
        if safe_form.validate_on_submit():
            safe_form.populate_obj(self)
            self.created_at = arrow.now()
            db.session.add(self)
            success = True
        return self, success

    @classmethod
    def create(cls, **kw):
        self = cls(**kw)
        if cls.is_exists(self.scientific_name,
                         self.rank_name,
                         self.kingdom_name):
            abort(409)
        self.created_at = arrow.now()
        db.session.add(self)
        return self

    @classmethod
    def retrieve(cls, scientific_name, rank_name, kingdom_name):
        try:
            self = cls.query.filter_by(
                scientific_name=scientific_name,
                rank_name=rank_name, kingdom_name=kingdom_name).one()
        except NoResultFound:
            abort(404, 'The requested taxon was not found.')
        return self

    @classmethod
    def retrieve_tsn(cls, tsn):
        try:
            self = cls.query.filter_by(itis_tsn=tsn).one()
        except NoResultFound:
            abort(404, 'The requested taxon was not found.')
        return self

    def form_update(self, unsafe_form):
        self._form = safe_form = TaxonForm(unsafe_form, obj=self)
        success = False
        if safe_form.validate_on_submit():
            safe_form.populate_obj(self)
            # forbid to edit scientific name though update
            # TODO: forbid to change rank and kingdom too?
            if orm_helpers.is_changed(self, 'scientific_name'):
                abort(403, 'Scientific name can not be changed.')
            if orm_helpers.is_changed(self):
                self.updated_at = arrow.now()
            success = True
        return self, success

    def update(self, **kw):
        for key, val in kw.iteritems():
            setattr(self, key, val)
        if orm_helpers.is_changed(self, 'scientific_name'):
            abort(403, 'Scientific name can not be changed.')
        if orm_helpers.is_changed(self):
            self.updated_at = arrow.now()
        return self


class TaxonForm(app.ModelForm):

    class Meta:
        model = Taxon
        exclude = ['created_at', 'updated_at']
        strip_string_fields = True

TaxonForm.submit = fields.SubmitField('Submit')
