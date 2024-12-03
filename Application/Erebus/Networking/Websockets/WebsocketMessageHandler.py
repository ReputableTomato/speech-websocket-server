import json

from Erebus.Networking.Router.Router import Router
from Erebus.Generic.Utilities.Comparison import Comparison

class WebsocketMessageHandler:

    @staticmethod
    async def process(websocket, request):
        """A method to process an incoming message.

        Args:
            websocket (Websocket): The websocket object.
            request: The user's request.
        """
        router = Router()

        try:
            request = json.loads(request)
        except ValueError:
            return await websocket.send(
                success = False,
                message = "Messages must be valid JSON.",
                type = router.context.constants.INVALID_JSON
            )

        route_validation = Comparison.validate_dictionary_values({
            "route": str
        }, request)

        if not route_validation["result"]:
            return await websocket.send(
                success = False,
                message = "You must select which route you would like to access.",
                type = router.context.constants.MISSING_PARAMETER
            )

        await router.process_request(websocket, route_validation['original'])