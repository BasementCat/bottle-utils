import json

import bottle

def JsonResponse(callback):
    return JsonResponsePlugin().apply(callback, None)

class JsonResponsePlugin(object):
    name    = 'JsonResponsePlugin'
    api     = 2

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            try:
                out = callback(*args, **kwargs)
                if isinstance(out, dict):
                    if 'result' in out or 'error' in out:
                        return out
                    return dict(result = out)
                elif isinstance(out, list):
                    return dict(result = out)
                else:
                    return out
            except bottle.HTTPResponse as e:
                if isinstance(e.body, dict):
                    message = e.body
                else:
                    message = dict(message = e.body, code = e.status_code)
                headers = [(k,v) for k,v in e.headers.items()]
                headers.append(('Content-Type', 'application/json'))
                raise bottle.HTTPResponse(json.dumps(dict(error = message)), e.status_code, headers = headers)
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
