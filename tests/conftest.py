import pytest
from config import create_app
from config.database import db as _db


@pytest.fixture(scope='session')
def app():
    app = create_app(test_cfg=True)
    return app


@pytest.fixture(autouse=True)
def _push_request_context(request, app):
    ctx = app.app_context()  # create context
    ctx.push()  # push

    def teardown():
        ctx.pop()  # pop

    request.addfinalizer(teardown)  # set teardown


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session', autouse=True)
def db(app):
    """
    Setup our database, this only gets executed once per session.

    :param app: Pytest fixture
    :return: SQLAlchemy database session
    """
    db = _db
    return db

