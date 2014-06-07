import json

import bottle

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

class JsonResponsePlugin(object):
    name    = 'JsonResponsePlugin'
    api     = 2

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            try:
                out = callback(*args, **kwargs)
                if isinstance(out, dict):
                    if out.keys() == ['result'] or out.keys == ['error']:
                        return out
                elif isinstance(out, list):
                    return dict(result = out)
                else:
                    return out
            except bottle.HTTPResponse as e:
                if isinstance(e.body, dict):
                    body = e.body
                else:
                    body = dict(message = e.body, code = e.status_code)
                headers = [(k,v) for k,v in e.headers.items()]
                headers.append(('Content-Type', 'application/json'))
                raise bottle.HTTPResponse(json.dumps(dict(error = body)), e.status_code, headers = headers)
        return wrapper

    @staticmethod
    def getErrorHandler(code):
        def wrapper(*args, **kwargs):
            return JsonResponsePlugin.errorHandler(code, *args, **kwargs)
        return wrapper

    @staticmethod
    def errorHandler(code, *args, **kwargs):
        return json.dumps({
            'error': {
                'code':     code,
                'message':  bottle.HTTP_CODES[code]
            }
        })

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
