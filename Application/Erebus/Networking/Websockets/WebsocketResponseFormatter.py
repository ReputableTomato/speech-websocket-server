import json

class WebsocketResponseFormatter:

    @staticmethod
    def json(**message) -> dict:
        return json.dumps(message)