import json

from Erebus.Context import Context
from Erebus.Generic.Utilities.Comparison import Comparison

from typing import Tuple

class ChannelMessageHandler:

    @staticmethod
    def parse(message) -> Tuple[bool, dict]:
        if message:
            key_validation_check = Comparison.validate_keys(["type"], message)

            if not key_validation_check["result"]:
                print("{} field missing from message. Skipping.".format(key_validation_check["key"]))

                return False

            if message["type"] == "message":
                return json.loads(message["data"])

        return False

    @staticmethod
    async def process(message):
        context = Context()
        key_validation_check = Comparison.validate_keys(["room", "payload"], message)

        if not key_validation_check["result"]:
            print("{} field missing from message. Skipping.".format(key_validation_check["key"]))

        for user_id in context.connection_handler.users:
            user = context.connection_handler.users[user_id]

            if message["room"] in user.account.rooms:
                await user.send_json(message["payload"])
 
        return