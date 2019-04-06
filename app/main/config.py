import os
from mailshake import SMTPMailer

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

USER_AGENT = "Telocam"

basedir = os.path.abspath(os.path.dirname(__file__))

BD_PASWORD = os.getenv('BD_PASWORD', '')
BD_NAME = os.getenv('BD_NAME', 'telocam')

POSTGRES = {
    'user': 'jorgegene',
    'db': 'jorgegene',
    'pw': 'telocam',
    'host': '127.0.0.1',
    'port': '5432',
}

mailer = SMTPMailer(
                host="smtp.unizar.es",
                port=587,
                username=719509,
                password="",  # TODO poner contraseña antes de correr el programa
                use_tls=True,
                use_ssl=None,
                timeout=None
            )


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + \
        BD_PASWORD + '@155.210.47.51:15432/telocam_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
