# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ('postgresql+psycopg2://'
                    'taxo:taxo@localhost:5432/taxonwiki')
    ASSETS_DEBUG = False
    ASSETS_CACHE = True
    ASSETS_MANIFEST = 'json'
    UGLIFYJS_EXTRA_ARGS = ['--compress', '--mangle']
    COMPASS_CONFIG = {
        'output_style': ':compressed'
    }


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    ASSETS_CACHE = False
    UGLIFYJS_EXTRA_ARGS = ['--compress']
    COMPASS_CONFIG = {
        'output_style': ':extended'
    }


class TestingConfig(Config):
    TESTING = True
