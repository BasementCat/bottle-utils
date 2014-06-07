# bottle-utils

Reusable components for bottle

## Responses

### JSON response handler

The json response handler is a plugin that provides three main features:
  * Returns dict or list responses as a JSON object: {"result": <output>}
    * If the response is a dict containing either "result" or "error", the result is returned as-is
  * Catches HTTPResponse exceptions (including the subclass HTTPError) and formats them as a JSON object: {"error": {"code": <http response code>, "message": <exception message>}}
  * Provides an error handler that can be used to replace the standard error handler with one that returns JSON objects
    * The handler must be manually applied for each error code to each app