import random
import string
import uuid

class Random:

    @staticmethod
    def string(self, length):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

    @staticmethod
    def uuid():
        return str(uuid.uuid4())