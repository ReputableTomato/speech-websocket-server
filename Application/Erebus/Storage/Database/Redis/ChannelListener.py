import asyncio

from Erebus.Context import Context
from Erebus.Storage.Database.Redis.ChannelMessageHandler import ChannelMessageHandler

class ChannelListener(Context):

    def __init__(self):
        self.__pubsub = self.redis.connection.pubsub()
        self.__message = None

    async def listen(self):
        # Subscribe to the global message channel.
        self.pubsub.subscribe("global")

        try:
            while True:
                self.message = self.pubsub.get_message()
                self.message = ChannelMessageHandler.parse(self.message)

                if self.message:
                    await ChannelMessageHandler.process(self.message)

                await asyncio.sleep(0.001)

        except Exception as error:
            print("An error occured while listening to the redis server: {}".format(error))

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        self.__message = message

    @property
    def pubsub(self):
        return self.__pubsub