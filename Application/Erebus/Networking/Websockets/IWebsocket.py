import json
import pprint
import tornado

from Erebus.Networking.Websockets.WebsocketResponseFormatter import WebsocketResponseFormatter
from tornado.httputil import HTTPHeaders

class IWebsocket:

    def __init__(self, websocket):
        self.__websocket = websocket
        self.__account = None
        self.__subscriptions = []
        self.__rooms = []

    @property
    def websocket(self):
        return self.__websocket

    @websocket.setter
    def websocket(self, websocket):
        self.__websocket = websocket

    @property
    def account(self):
        return self.__account

    @account.setter
    def account(self, account):
        self.__account = account

    @property
    def subscriptions(self):
        return self.__subscriptions

    @subscriptions.setter
    def subscriptions(self, subscriptions):
        self.__subscriptions = subscriptions

    @property
    def rooms(self) -> list:
        return self.__rooms

    @rooms.setter
    def rooms(self, rooms) -> None:
        self.__rooms = rooms

    @property
    def headers(self) -> HTTPHeaders:
        return self.websocket.request.headers

    @property
    def websocket_id(self) -> str:
        return self.websocket.websocket_id

    @websocket_id.setter
    def websocket_id(self, websocket_id) -> None:
        self.websocket.websocket_id = websocket_id

    @property
    def connection_type(self) -> str:
        return self.websocket.connection_type if hasattr(self.websocket, "connection_type") else None

    @connection_type.setter
    def connection_type(self, connection_type) -> None:
        self.websocket.connection_type = connection_type

    @property
    def ip_address(self) -> str:
        return self.websocket.request.headers['X-Real-Ip'] if "X-Real-Ip" in self.websocket.request.headers else self.websocket.request.remote_ip

    async def send_raw(self, raw_data) -> bool:
        try:
            await self.websocket.write_message(raw_data, True)

            return True
        except tornado.websocket.WebsocketClosedError as error:
            print("Could not send message to websocket client: {}".format(error))

            return False


    async def send(self, **message) -> bool:
        formatted_message = WebsocketResponseFormatter.json(**message)

        return await self.send_json(formatted_message)

    async def send_json(self, json_data) -> bool:
        try:
            await self.websocket.write_message(json_data)

            return True
        except tornado.websocket.WebsocketClosedError as error:
            print("Could not send json message to websocket client: {}".format(error))

            return False

    async def subscription_send(self, subscription_key, formatted_message) -> bool:
        if subscription_key in self.subscriptions:
            return await self.send_json(formatted_message)

        return False