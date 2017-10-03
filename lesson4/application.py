#uwsgi --http :9090 --wsgi-file ./lesson4/application.py
from lesson4.FrameWork import routing

routes = {}


@routing.route('/', routes=routes)
def hello():
    return [b"Hello World"]


@routing.route('/test', routes=routes)
def test():
    return [b"Test"]


def application(env, start_response):
    try:
        routes[env['REQUEST_URI']]
        start_response('200 OK', [('Content-Type', 'text/html')])
        return routes[env['REQUEST_URI']]()
    except KeyError:
        start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
        return [b"Not Found"]
