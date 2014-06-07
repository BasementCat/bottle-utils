# bottle-utils

Reusable components for bottle

## Responses

### response.JsonResponsePlugin

The JSON response plugin is a plugin that provides three main features:
  * Returns dict or list responses as a JSON object: {"result": <output>}
    * If the response is a dict containing either "result" or "error", the result is returned as-is
  * Catches HTTPResponse exceptions (including the subclass HTTPError) and formats them as a JSON object: {"error": {"code": <http response code>, "message": <exception message>}}
  * Provides an error handler that can be used to replace the standard error handler with one that returns JSON objects
    * The handler must be manually applied for each error code to each app

### response.SQLAlchemyNotFoundPlugin

The SQLAlchemy not found plugin converts SQLAlchemy not found exceptions to 404s.  This does NOT raise an error on import if SQLAlchemy is not installed but if it is not, applying the plugin will break!  Apply within the JsonResponsePlugin to turn not found objects into a nicely formatted JSON error message.