import os
basedir = os.path.abspath(os.path.dirname(__file__))


POSTGRES = {
    'user': 'jorgegene',
    'db': 'jorgegene',
    'pw': 'telocam',
    'host': 'localhost',    
    #'user': 'telocam',
    #'db': 'telocam',
    #'pw': 'passtelocam',
    #'host': '155.210.47.51',
    'port': '5432',
}

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = True