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

class Pagination(object):
    def __init__(self, query, page=None, per_page=None, default_per_page=25):
        self.query = query
        self.count = query.count()

        try:
            self.page = int(page or bottle.request.query.get('page', 1))
        except ValueError:
            self.page = 1

        try:
            self.per_page = int(per_page or bottle.request.query.get('per_page', default_per_page))
        except ValueError:
            self.per_page = default_per_page

        self.pages = int(math.ceil(self.count / float(self.per_page)))

    @property
    def items(self):
        return self.query.offset(self.per_page * (self.page - 1)).limit(self.per_page).all()

    @property
    def json_response(self):
        return {
            'result': [v.to_json() if hasattr(v, 'to_json') else str(v) for v in self.items],
            'pagination': {
                'page': self.page,
                'per_page': self.per_page,
                'count': self.count,
                'pages': self.pages,
            }
        }
