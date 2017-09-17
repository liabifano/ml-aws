import os

MODEL_VERSION = open(os.path.join(os.path.abspath(os.path.join(__file__, '../../../..')), 'VERSION')).read()
RESOURCES_PATH = os.path.join(os.path.abspath(os.path.join(__file__, '../../../..')), 'resources', 'model')
MODEL_PATH = os.path.join(RESOURCES_PATH, 'trained_model_{}.pkl'.format(MODEL_VERSION))
FEATURES_MODEL = ['sepal_length', 'sepal_width', 'pental_length', 'pental_width']


class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_HOST', 'sqlite://')
    DEBUG = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DEBUG = None
