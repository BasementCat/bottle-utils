import bottle

def setup(main_app, sub_apps = [], plugins = [], error_handlers = [], error_handler_generators = []):
    real_sub_apps = sub_apps[:]
    real_sub_apps.append(main_app)
    for app_data in real_sub_apps:
        if isinstance(app_data, list):
            app, mountpoint = app_data
        else:
            app = app_data
            mountpoint = None

        if app is not main_app and mountpoint is not None:
            main_app.mount(mountpoint, app)

        for plugin in plugins:
            app.install(plugin)

        for handler_data in error_handlers:
            if isinstance(handler_data, list):
                range_, handler = handler_data
            else:
                range_ = range(300, 599)
                handler = handler_data

            for code in bottle.HTTP_CODES:
                if code in range_:
                    app.error(code)(handler)

        for handler_data in error_handler_generators:
            if isinstance(handler_data, list):
                range_, handler = handler_data
            else:
                range_ = range(300, 599)
                handler = handler_data

            for code in bottle.HTTP_CODES:
                if code in range_:
                    app.error(code)(handler(code))