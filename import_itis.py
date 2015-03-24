#! /usr/bin/env python
# -*- coding: utf-8 -*-

from taxonwiki import init_app

app = init_app('development')

with app.app_context():
    from taxonwiki.tasks import itis

    with itis.itis_connect() as conn:
        itis.import_kingdoms(conn)
        itis.import_ranks(conn)
        itis.import_taxa(conn, 3001)

    app.db.session.commit()
