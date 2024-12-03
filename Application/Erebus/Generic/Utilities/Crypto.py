import secrets
import random
import string
import base64

class Crypto:

    @staticmethod
    def random_id(length):
        return secrets.token_hex(length)

    @staticmethod
    def random_string(length):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def encode(string):
        return base64.b64encode(string).decode("latin-1")

    @staticmethod
    def decode(string):
        return base64.b64decode(string.encode("latin-1"))