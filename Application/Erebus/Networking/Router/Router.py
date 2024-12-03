import time
import traceback
import re

from Erebus.Context import Context
from Erebus.Networking.UserTypes.UserAccount import UserAccount
from Erebus.Generic.Utilities.Comparison import Comparison

class Router:

    __instance = None

    def __init__(self):

        if __class__.__instance != None:
            self = __class__.__instance
        else:
            __class__.__instance = self

            self._routes = {
                "standard": {},
                "regex": {}
            }
            self._context = Context()

    async def process_request(self, websocket, request):
        route = request["route"]
        decoded_token = None
        route_exists = False

        if route in self.routes["standard"]:
            route_exists = True
            route_config = self.routes["standard"][route]
        else:
            for regex_route in self.routes["regex"]:
                match_result = re.match(regex_route, route)

                if match_result:
                    route_exists = True
                    route_config = self.routes["regex"][regex_route]
                    
                    # Map our matched parameters to their string values.
                    for group_index, parameter_name in enumerate(route_config["map"].keys()):
                        # If the parameter is a number, we need to convert our string value to an integer.
                        if route_config["map"][parameter_name] == "number":
                            parameter_value = int(match_result.group(group_index + 1))
                        elif route_config["map"][parameter_name] == "word":
                            # By default, our value is a string.
                            parameter_value = match_result.group(group_index + 1)

                        request[parameter_name] = parameter_value

        if not route_exists:
            return await websocket.send(
                success = False,
                message = "You must provide a valid route.",
                type = self.context.constants.INVALID_ROUTE
            )

        del request["route"]

        if "login_required" in route_config and route_config["login_required"]:
            if "token" not in request:
                return await websocket.send(
                    success = False,
                    message = "Authentication is required for this route.",
                    type = self.context.constants.TOKEN_MISSING
                )

            try:
                decoded_token = await self.context.jwt_controller.decode(request["token"])
            except Exception as error:
                return await websocket.send(
                    success = False,
                    message = "Invalid token provided.",
                    type = self.context.constants.INVALID_TOKEN
                )

            current_time = int(time.time())

            if current_time > decoded_token["expire_time"]:
                return await websocket.send(
                    success = False,
                    message = "Your token has expired",
                    type = self.context.constants.EXPIRED_TOKEN
                )

            if not websocket.account:
                if decoded_token["type"] == "user":
                    user_account = UserAccount()
                    user_account.get(id = decoded_token["id"])
                    websocket.account = user_account

                    await self.context.connection_handler.register_connection(websocket, "user")

            del request["token"]
        
        try:
            route_instance = route_config["controller"]

            if hasattr(route_instance, "configuration") and "requirements" in route_instance.configuration:
                requirements = route_instance.configuration["requirements"].copy()
                request_copy = request.copy()
                route_validation = Comparison.validate_dictionary_values(requirements, request_copy)

                if not route_validation["result"]:
                    message = route_validation["error"] if "error" in route_validation and route_validation["error"] else "Missing parameter"

                    return await websocket.send(
                        success = False,
                        message = message,
                        param = route_validation["attribute_name"],
                        param_type = route_validation["attribute_type"],
                        type = self.context.constants.MISSING_PARAMETER
                    )

            await route_instance.setup(websocket, request, decoded_token)
            await route_instance.main()
        except Exception as error:
            traceback.print_exc()

    @property
    def routes(self):
        return self.instance()._routes

    @property
    def context(self):
        return self.instance()._context

    @staticmethod
    def add_route(path, config = {}, route_type = "standard"):
        if path in Router.instance()._routes["standard"] or path in Router.instance()._routes["regex"]:
            raise Exception("A route for '{}' already exists.".format(path))

        Router.instance()._routes[route_type][path] = config

    @staticmethod
    def instance():
        if __class__.__instance == None:
            return __class__()

        return __class__.__instance