import json

import bottle

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