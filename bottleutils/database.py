import math
import datetime

import sqlalchemy
from sqlalchemy.orm.attributes import InstrumentedAttribute
import bottle

try:
    import arrow
except ImportError:
    pass

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
    maker       = None

    def __init__(self, engine):
        self.engine = engine
        self.maker = sqlalchemy.orm.sessionmaker(bind = self.engine)

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            bottle.request.sa_session = self.maker()
            out = callback(*args, **kwargs)
            bottle.request.sa_session.close()
            return out
        return wrapper

class SQLAlchemyJsonMixin(object):
    def to_json(self):
        out = {}
        for attrname, clsattr in vars(self.__class__).items():
            if isinstance(clsattr, InstrumentedAttribute):
                attr = getattr(self, attrname)

                try:
                    if isinstance(attr, arrow.arrow.Arrow):
                        attr = str(attr)
                except NameError:
                    pass

                if isinstance(attr, datetime.datetime):
                    attr = str(attr)
                elif isinstance(attr, self.__class__):
                    continue

                out[attrname] = attr
        return out
