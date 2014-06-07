# bottle-utils

Reusable components for bottle

## Responses

### response.JsonResponsePlugin

The JSON response plugin is a plugin that provides three main features:
  * Returns dict or list responses as a JSON object: {"result": <output>}
    * If the response is a dict containing either "result" or "error", the result is returned as-is
  * Catches HTTPResponse exceptions (including the subclass HTTPError) and formats them as a JSON object: {"error": {"code": <http response code>, "message": <exception message>}}
  * Provides an error handler that can be used to replace the standard error handler with one that returns JSON objects
    * The handler must be manually applied for each error code to each app, except as shown below

## SQLAlchemy

### sqlalchemy.SQLAlchemyNotFoundPlugin

The SQLAlchemy not found plugin converts SQLAlchemy not found exceptions to 404s.  The SQLAlchemy package must be installed, and is NOT a requirement of this package as a whole!  Make sure it is installed or ImportError will be raised.  Apply within the JsonResponsePlugin to turn not found objects into a nicely formatted JSON error message.

## Apps

### apps.setup

Set up a collection of apps.  The function accepts the following arguments:
  * main_app (required): "main" app on which other apps are mounted
  * sub_apps (optional): List containing either plain application instances (which are not mounted anywhere) or lists containing [app, mountpoint], where the app is mounted to main_app at mountpoint.  The main_app is automatically added to this list - do not add it yourself.
  * plugins (optional): list of plugins to install to all apps
  * error_handlers (optional): List containing either error handler callbacks, or lists containing [range, handler] where handler is applied to all error codes in range (default range is 300-599)
  * error_handler_generators (optional): List containing either methods that generate error handler callbacks, or lists containing [range, handler_generator] where handler_generator(code) is applied to all error codes in range (default range is 300-599)

error_handler_generators can be used to apply the JSON response error handler:
    setup(mainapp, [otherapp], error_handler_generators = [JsonResponsePlugin.getErrorHandler])
