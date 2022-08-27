"""Flask configuration."""


class Config:
    """Base config."""
    SECRET_KEY = "123456789"
    JSON_SORT_KEYS = False
    SERVER_NAME = "localhost"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost/flask"
    SQLALCHEMY_BINDS = {
        'master': "mysql+mysqlconnector://root:root@localhost/flask",
        'slave': "mysql+mysqlconnector://flask_slv:root@localhost/flask_slv"
    }


class TestConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost/flask"
    SQLALCHEMY_BINDS = {
        'master': "mysql+mysqlconnector://root:root@localhost/flask",
        'slave': "mysql+mysqlconnector://flask_slv:root@localhost/flask_slv"
    }
