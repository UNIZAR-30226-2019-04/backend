import os
from mailshake import SMTPMailer

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

USER_AGENT = "Telocam"

basedir = os.path.abspath(os.path.dirname(__file__))


POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'postgres')
SECRET_KEY = os.getenv('SECRET_KEY', 'jorgegene')

POSTGRES = {
    'user': POSTGRES_USER,
    'db': POSTGRES_DB,
    'pw': POSTGRES_PASSWORD,
    'host': '127.0.0.1',  # docker-compose creates a hostname alias with the service name
    'port': '5432',
}

mailer = SMTPMailer(
    host="smtp.gmail.com",
    port=587,
    username="telocam.soporte",
    password="telocam1234",
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
        POSTGRES_PASSWORD + '@155.210.47.51:15432/telocam_test'
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
