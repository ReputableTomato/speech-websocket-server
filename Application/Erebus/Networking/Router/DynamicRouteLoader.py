from Erebus.Context import Context
from Erebus.Networking.Router.Router import Router
from Erebus.Networking.Router.PathFormatter import PathFormatter
from Erebus.Networking.Router.RouteInitialiser import RouteInitialiser

class DynamicRouteLoader:
    
    def __init__(self):
        self._context = Context()
        self._router = Router()

    def setup_routes(self, route_configuration):
        regex_route = False

        for route_type in route_configuration.keys():
            for route_location, route_config in route_configuration[route_type].items():
                if "controller" in route_config:
                    route_path = PathFormatter.format(route_config["controller"], skip_capitalization = True)
                    regex_route = True
                else:
                    route_path = PathFormatter.format(route_location)

                route_config["controller"] = RouteInitialiser.route_instance(route_path)
                route_location = "/{}".format(route_location)

                if regex_route:
                    self.router.add_route(route_location, route_config, "regex")
                else:
                    self.router.add_route(route_location, route_config, "standard")

                regex_route = False

    @property
    def context(self):
        return self._context

    @property
    def router(self):
        return self._router