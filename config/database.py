from functools import partial
from flask_sqlalchemy import SQLAlchemy, get_state
from sqlalchemy import event, orm
from sqlalchemy.engine import Engine
import time
from flask import current_app
from utils.logger import LoggerUtils


class RoutingSession(orm.Session):
    """ Routing class"""

    def __init__(self, db, autocommit=False, autoflush=True, **options):
        """ init function """
        self.app = db.get_app()
        self.db = db
        self._bind_name = None
        orm.Session.__init__(
            self, autocommit=autocommit, autoflush=autoflush,
            bind=db.engine,
            binds=db.get_binds(self.app),
            **options,
        )

    def get_bind(self, mapper=None, clause=None):
        """ get binds """
        try:
            state = get_state(self.app)
        except (AssertionError, AttributeError, TypeError) as err:
            current_app.logger.info(
                'cant get configuration. default bind. Error:' + err)
            return orm.Session.get_bind(self, mapper, clause)

        # If there are no binds configured, use default SQLALCHEMY_DATABASE_URI
        if not state or not self.app.config['SQLALCHEMY_BINDS']:
            return orm.Session.get_bind(self, mapper, clause)

        # if want to user exact bind
        if self._bind_name:
            obj = state.db.get_engine(self.app, bind=self._bind_name)
        else:
            # if no bind is used connect to default
            obj = orm.Session.get_bind(self, mapper, clause)
        return obj

    def using_bind(self, name):
        """ using bind """
        bind_session = RoutingSession(self.db)
        vars(bind_session).update(vars(self))
        # pylint: disable=protected-access
        bind_session._bind_name = name
        orm.session.Session.info.bind_info = name
        return bind_session


class RouteSQLAlchemy(SQLAlchemy):
    """ Routing SQLAlchemy"""

    def __init__(self, *args, **kwargs):
        """ init """
        SQLAlchemy.__init__(self, *args, **kwargs)
        self.session.using_bind = lambda s: self.session().using_bind(s)

    def create_scoped_session(self, options=None):
        """ create scoped session """
        if options is None:
            options = {}
        scopefunc = options.pop('scopefunc', None)
        return orm.scoped_session(
            partial(RoutingSession, self, **options),
            scopefunc=scopefunc,
        )


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement,
                          parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement,
                         parameters, context, executemany):
    bind_info = (lambda s: s.__getattribute__('bind_info') if hasattr(s, 'bind_info') else 'master')\
        (orm.session.Session.info)
    orm.session.Session.info.bind_info = None
    total = time.time() - conn.info['query_start_time'].pop(-1)
    LoggerUtils.query_logger(bind_info, statement, total)


db = RouteSQLAlchemy()
