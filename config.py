import os


class Config:

    SECRET_KEY = 'testkey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:password@127.0.0.1:5432/testdatab'
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    DEBUG = False


class DockerDevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://testuser:password@postgres/testdatab'
    DEBUG = True


config = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'docker': DockerDevConfig
}
