#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask.ext.script import Manager
from flask.ext.alembic.cli import script as Migrations
from flask.ext.assets import ManageAssets

from taxonwiki import app as app_module

app = app_module.init_app('development')

manager = Manager(app)
manager.add_command('migrate', Migrations.manager)
manager.add_command('assets', ManageAssets())


if __name__ == '__main__':
    manager.run()
