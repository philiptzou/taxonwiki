# -*- coding: utf-8 -*-

import urlparse
import sqlalchemy
from contextlib import contextmanager
from flask import current_app as app
from werkzeug.exceptions import NotFound


@contextmanager
def itis_connect():
    uri = urlparse.urlparse(app.config['DATABASE_URI'])
    uri = uri[0:2] + ('ITIS',) + uri[3:]
    uri = urlparse.urlunparse(uri)
    engine = sqlalchemy.engine.create_engine(uri, server_side_cursors=True)
    conn = engine.connect()
    try:
        yield conn
    finally:
        conn.close()


def get_kingdoms(conn):
    result = conn.execute('SELECT kingdom_id, kingdom_name FROM kingdoms')
    return {idx: {'name': name.rstrip()}
            for idx, name in result}


def get_ranks(conn):
    result = conn.execute('SELECT t1.rank_id, kingdom_name, t1.rank_name, '
                          'dir.rank_name, req.rank_name '
                          'FROM taxon_unit_types t1, kingdoms, '
                          'taxon_unit_types dir, taxon_unit_types req '
                          'WHERE kingdoms.kingdom_id = t1.kingdom_id AND '
                          'dir.rank_id = t1.dir_parent_rank_id AND '
                          'dir.kingdom_id = t1.kingdom_id AND '
                          'req.rank_id = t1.req_parent_rank_id AND '
                          'req.kingdom_id = t1.kingdom_id')
    return [{'name': name.rstrip(),
             'kingdom_name': kname.rstrip(),
             'direct_parent_rank_name': dprn.rstrip(),
             'required_parent_rank_name': rprn.rstrip(),
             'ordinal': idx}
            for idx, kname, name, dprn, rprn in result]


def norm_status(status):
    return {
        'accepted': u'valid',
        'not accepted': u'invalid',
        'valid': u'valid',
        'invalid': u'invalid'}[status]


def iter_taxa(conn):
    result = conn.execute('SELECT t.complete_name, t.name_usage, '
                          't.unaccept_reason, t.tsn, t.parent_tsn, '
                          'r.rank_name, k.kingdom_name, a.taxon_author '
                          'FROM taxonomic_units t LEFT JOIN '
                          'taxon_authors_lkp a ON '
                          'a.taxon_author_id = t.taxon_author_id, '
                          'taxon_unit_types r, kingdoms k '
                          'WHERE r.rank_id = t.rank_id AND '
                          'r.kingdom_id = t.kingdom_id AND '
                          'k.kingdom_id = t.kingdom_id AND '
                          "(t.name_usage='valid' OR t.name_usage='accepted') "
                          'ORDER BY t.kingdom_id, t.rank_id')
    for (sname, status, reason, tsn, parent_tsn,
         rname, kname, author) in result:
        yield {
            'scientific_name': sname.rstrip(),
            'status': norm_status(status),
            'invalid_reason': reason.rstrip() if reason else None,
            'itis_tsn': tsn,
            'parent_tsn': parent_tsn,
            'rank_name': rname.rstrip(),
            'kingdom_name': kname.rstrip(),
            'author_abbr': author.rstrip() if author else None
        }


def import_kingdoms(itis_conn):
    kingdoms = get_kingdoms(itis_conn)
    for kd in kingdoms.itervalues():
        kingdom = app.models.Kingdom(name=kd['name'])
        app.db.session.merge(kingdom)
    app.db.session.flush()


def import_ranks(itis_conn):
    ranks = get_ranks(itis_conn)
    for rk in ranks:
        rank = app.models.Rank(name=rk['name'],
                               kingdom_name=rk['kingdom_name'],
                               ordinal=rk['ordinal'])
        app.db.session.merge(rank)
    app.db.session.flush()
    for rk in ranks:
        rank = app.models.Rank(**rk)
        app.db.session.merge(rank)
    app.db.session.flush()


def import_taxa(itis_conn, test_limit=-1):
    Taxon = app.models.Taxon
    for tx in iter_taxa(itis_conn):
        if not test_limit:
            break
        test_limit -= 1
        parent_tsn = tx.pop('parent_tsn')
        sname = tx['scientific_name']
        rname = tx['rank_name']
        kname = tx['kingdom_name']
        try:
            taxon = Taxon.retrieve(sname, rname, kname)
            # TODO: propose but not apply changes if it's modified
            taxon.update(**tx)
        except NotFound:
            taxon = Taxon.create(**tx)
        if parent_tsn != 0:
            print tx['itis_tsn'], parent_tsn
            try:
                parent = Taxon.retrieve_tsn(parent_tsn)
            except:
                print Taxon.query.all()
                raise
            taxon.parent_id = parent.id
        app.db.session.flush()
