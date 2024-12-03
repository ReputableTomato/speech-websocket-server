class RouteInitialiser:

    @staticmethod
    def route_instance(route_path):
        module_path = "Routes.{}".format(route_path)
        module = __import__(module_path, fromlist = ["Route"])

        return getattr(module, "Route")()