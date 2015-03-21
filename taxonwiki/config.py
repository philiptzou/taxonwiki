# -*- coding: utf-8 -*-


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = ('postgresql+psycopg2://'
                    'taxo:taxo@localhost:5432/taxonwiki')


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
