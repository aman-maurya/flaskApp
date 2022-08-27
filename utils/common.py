from pathlib import Path
from flask import current_app


class CommonUtils:
    @classmethod
    def project_root_dir(cls):
        return Path(__file__).parent.parent

    @classmethod
    def is_production_env(cls):
        return current_app.config['FLASK_ENV'] == 'production'

    @classmethod
    def is_development_env(cls):
        return current_app.config['FLASK_ENV'] == 'development'

    @classmethod
    def is_testing_env(cls):
        return current_app.config['FLASK_ENV'] == 'testing'
