import time
import json

from Erebus.Context import Context

class Base:

    async def setup(self, websocket, request, decoded_token):
        self._websocket = websocket
        self._request = request
        self._decoded_token = decoded_token
        self._context = Context()

        self._collection_name = None
        self._query = {}

    @property
    def websocket(self):
        return self._websocket

    @property
    def request(self):
        return self._request

    @property
    def decoded_token(self):
        return self._decoded_token

    @property
    def context(self):
        return self._context

    @property
    def database_store(self):
        return self.context.database_store

    @property
    def database(self):
        return self.context.database

    @property
    def constants(self):
        return self.context.constants

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def now(self):
        return int(time.time())

    async def publish(self, **kwargs):
        self.context.redis.connection.publish("global", json.dumps(kwargs))