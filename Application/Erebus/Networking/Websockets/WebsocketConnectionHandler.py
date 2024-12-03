import json

from Erebus.Configuration import Configuration
from Erebus.Networking.Constants import Constants
# from Erebus.Console.ConsoleOutput import ConsoleOutput
from Erebus.Generic.Utilities.Crypto import Crypto
from Erebus.Networking.Websockets.WebsocketResponseFormatter import WebsocketResponseFormatter

class WebsocketConnectionHandler:

    __instance = None

    def __init__(self):
        if __class__.__instance != None:
            raise Exception("The connection handler cannot be initialised more than once.")
        else:
            __class__.__instance = self

            self._unauthenticated_connections = {}
            self._nodes = {}
            self._users = {}
            self._connection_count = 0

    @staticmethod
    def on_open(websocket):
        while True:
            websocket_id = Crypto.random_id(
                Configuration.instance().application_details["websocket_id_length"]
            )

            if websocket_id not in __class__.instance()._unauthenticated_connections:
                break

        websocket.websocket_id = websocket_id

        __class__.instance()._unauthenticated_connections[websocket_id] = websocket
        __class__.instance()._connection_count += 1

        # ConsoleOutput.connection_update(
        #     "Client connected",
        #     __class__.instance()._connection_count,
        #     len(__class__.instance()._unauthenticated_connections),
        #     len(__class__.instance()._users),
        #     len(__class__.instance()._nodes)
        # )

        # ConsoleOutput.print("{} has connected.".format(websocket.ip_address))

    @staticmethod
    async def on_close(websocket):
        if websocket.connection_type:
            if websocket.connection_type == "user":
                __class__.instance()._users.pop(websocket.websocket_id)

                # ConsoleOutput.print("{} has disconnected ({}).".format(websocket.account.username, websocket.ip_address))
            elif websocket.connection_type == "node":
                await __class__.instance().publish(
                    owner_id = websocket.account.owner_id,
                    message = "Node disconnected.",
                    node_id = websocket.account.id,
                    node_identifier = websocket.account.identifier,
                    type = Constants().NODE_DISCONNECTED
                )

                # ConsoleOutput.print("{} has disconnected ({}).".format(websocket.account.username, websocket.ip_address))

                __class__.instance()._nodes.pop(websocket.websocket_id)
        else:
            __class__.instance()._unauthenticated_connections.pop(
                websocket.websocket_id
            )

        __class__.instance()._connection_count -= 1

        # ConsoleOutput.connection_update(
        #     "Client disconnected",
        #     __class__.instance()._connection_count,
        #     len(__class__.instance()._unauthenticated_connections),
        #     len(__class__.instance()._users),
        #     len(__class__.instance()._nodes)
        # )

    @staticmethod
    async def register_connection(websocket, connection_type):
        websocket.connection_type = connection_type

        if websocket.websocket_id in __class__.instance()._unauthenticated_connections:
            __class__.instance()._unauthenticated_connections.pop(websocket.websocket_id)

        if connection_type == "user":
            __class__.instance()._users[websocket.websocket_id] = websocket

            # ConsoleOutput.connection_update(
            #     "User logged in.",
            #     __class__.instance()._connection_count,
            #     len(__class__.instance()._unauthenticated_connections),
            #     len(__class__.instance()._users),
            #     len(__class__.instance()._nodes)
            # )
        elif connection_type == "node":
            await __class__.instance().publish(
                owner_id = websocket.account.owner_id,
                message = "Node connected.",
                node_id = websocket.account.id,
                node_identifier = websocket.account.identifier,
                type = Constants().NODE_CONNECTED
            )

            # ConsoleOutput.connection_update(
            #     "Node registered",
            #     __class__.instance()._connection_count,
            #     len(__class__.instance()._unauthenticated_connections),
            #     len(__class__.instance()._users),
            #     len(__class__.instance()._nodes)                
            # )

            __class__.instance()._nodes[websocket.websocket_id] = websocket

    @staticmethod
    def get_subscribers(owner_id):
        subscribers = []

        for user in __class__.instance()._users:
            user = __class__.instance()._users[user]

            if user.account.id == owner_id:
                subscribers.append(user)

        return subscribers

    @staticmethod
    async def notify_all(message):
        for websocket_id, websocket in __class__.instance()._unauthenticated_connections.items():
            await websocket.send(message)

        for websocket_id, websocket in __class__.instance()._users.items():
            await websocket.send(message)

        for websocket_id, websocket in __class__.instance()._nodes.items():
            await websocket.send(message)

    @staticmethod
    async def publish(**kwargs):
        owner_id = kwargs["owner_id"]
        del kwargs["owner_id"]
        message = WebsocketResponseFormatter.json(**kwargs)

        subscribers = __class__.instance().get_subscribers(owner_id)

        for subscriber in subscribers:
            await subscriber.subscription_send("connection_alerts", message)

    @property
    def connection_count(self):
        return self._connection_count

    @property
    def nodes(self):
        return self._nodes

    @property
    def users(self):
        return self._users

    @staticmethod
    def instance():
        if __class__.__instance == None:
            return __class__()

        return __class__.__instance