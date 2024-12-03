import asyncio
import tornado
import tornado.ioloop
import json
import curses

from tornado import websocket

from Erebus.Context import Context
from Erebus.Networking.Websockets.WebsocketMessageHandler import WebsocketMessageHandler
from Erebus.Networking.Websockets.IWebsocket import IWebsocket
from Erebus.Networking.Router.DynamicRouteLoader import DynamicRouteLoader
from Erebus.Storage.Database.Redis.ChannelListener import ChannelListener

class Websocket_Server(websocket.WebSocketHandler):

    def initialize(self):
        self.context = Context.instance()
        self.websocket = IWebsocket(self)

    async def open(self):
        self.context.connection_handler.on_open(self.websocket)

    async def on_message(self, message):
        await WebsocketMessageHandler.process(self.websocket, message)

    def on_close(self):
        io_loop = tornado.ioloop.IOLoop.current()
        io_loop.spawn_callback(self.context.connection_handler.on_close, self.websocket)

    def check_origin(self, origin):
        return True

if __name__ == "__main__":
    context = Context()
    route_loader = DynamicRouteLoader()
    route_configuration = context.file_handle.read_yaml_file(
        "{}{}".format(context.root_path, "Routes.yml")
    )
    route_loader.setup_routes(route_configuration)

    try:
        application = tornado.httpserver.HTTPServer(
            tornado.web.Application([
                (r"/", Websocket_Server)
            ])
        )

        application.listen(context.configuration.application_details["port"])

        try:
            tornado.ioloop.IOLoop.instance().start()
        except KeyboardInterrupt:
            curses.echo()
            curses.nocbreak()
            curses.endwin()

            print("Shutting down server.")
    except Exception as error:
        print("Could not start server: {}".format(error))