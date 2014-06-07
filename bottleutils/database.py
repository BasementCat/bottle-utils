import sqlalchemy

class SQLAlchemyNotFoundPlugin(object):
    name    = 'SQLAlchemyNotFoundPlugin'
    api     = 2

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            try:
                return callback(*args, **kwargs)
            except sqlalchemy.orm.exc.NoResultFound:
                raise bottle.HTTPError(404, "Item not found")
        return wrapper

class SQLAlchemySession(object):
    name    = 'SQLAlchemySession'
    api     = 2

    engine      = None
    autocommit  = True
    maker       = None

    def __init__(self, engine, autocommit = True):
        self.engine = engine
        self.autocommit = autocommit
        self.maker = sqlalchemy.orm.sessionmaker(bind = self.engine)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            bottle.request.sa_session = self.maker()
            out = callback(*args, **kwargs)
            if self.autocommit:
                bottle.request.sa_session.commit()
            bottle.request.sa_session.close()
            return out
        return wrapper