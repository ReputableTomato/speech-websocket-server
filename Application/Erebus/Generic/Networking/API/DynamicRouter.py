import tornado.web

from Generic.Context import Context

class GetHandler(tornado.web.RequestHandler):

    def get(self, path):
        """A method for handling an incoming get request.

        Args:
            path (string): The path being accessed.
        """
        resources = {}

        if path not in resources:
            raise tornado.web.HTTPError(404)

        self.finish(resources[path])

class PostHandler(tornado.web.RequestHandler):

    def post(self, path):
        """A method for handling an incoming post request.

        Args:
            path (string): The path being accessed.
        """
        resources[path] = self.request.body

class DynamicRouter(tornado.routing.Router, Context):

    def __init__(self, application):
        super().__init__()

        self._application = application

    @property
    def application(self):
        """An accessor method for the application instance

        returns:
            application (object): The application object.
        """
        return self._application

    def find_handler(self, request, **kwargs):
        """A method for specifying a handler for each request type.

        returns:
            HTTPMessageDelegate (HTTPMessageDelegate): A method that handles
            the output of our custom handler.
        """
        handler = GetHandler if request.method == "GET" else PostHandler

        return self._application.get_handler_delegate(
            request,
            handler,
            path_args = [
                request.path
            ]
        )