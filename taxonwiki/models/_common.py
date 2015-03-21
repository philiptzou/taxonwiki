# -*- coding: utf-8 -*-

from flask import current_app as app

ENUM_ORGANISM = app.db.Enum('animal', 'bacterial', 'fungi',
                            'plant', 'protist', 'virus',
                            name='organism_enum')
