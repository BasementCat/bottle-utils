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
