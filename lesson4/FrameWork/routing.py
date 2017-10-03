def route(route='/'):
    def decorator(function, env, start_response):
        def wrapped():
            start_response('200 OK', [('Content-Type', 'text/html')])
            return function
        return wrapped
    return decorator