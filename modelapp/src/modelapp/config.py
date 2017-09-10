import os


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_HOST', 'sqlite://')
    DEBUG = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DEBUG = None
