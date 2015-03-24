#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask import url_for
from flask.ext.script import Manager
from flask.ext.alembic.cli import script as Migrations
from flask.ext.assets import ManageAssets

from taxonwiki import init_app

app = init_app('development')

manager = Manager(app)
manager.add_command('migrate', Migrations.manager)
manager.add_command('assets', ManageAssets())


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{0:40s} {1:30s} {2}"
                              .format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print line


if __name__ == '__main__':
    manager.run()
