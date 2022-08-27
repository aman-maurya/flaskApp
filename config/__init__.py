from werkzeug.exceptions import HTTPException
from flask import Flask, json
from flask_restful import Api
from resources.users import user_v1
from config.database import db
from config.setting import DevConfig, TestConfig
from flask_migrate import Migrate

app = Flask(__name__, instance_relative_config=True)


def create_app(test_cfg=False):
    if test_cfg:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(DevConfig)

    app.config.from_pyfile('settings.py', silent=True)
    api = Api(app, catch_all_404s=True, serve_challenge_on_401=True)
    # api.add_resource(User, '/user')
    api.init_app(app)
    db.init_app(app)
    Migrate(app, db)
    app.register_blueprint(user_v1, url_prefix='/v1')

    return app


# def log_exception(sender, exception, **extra):
#     """ Log an exception to our logging framework """
#     _traceback = ''.join(traceback.format_tb(exception.__traceback__))
#     sender.logger.debug('Got exception during processing: %s', exception)
#
#
# # got_request_exception.connect(log_exception, app)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "status": 0,
        "error": {
            "code": e.error_code,
            "name": e.name,
            "message": e.description,
        }
    })
    response.content_type = "application/json"
    return response
