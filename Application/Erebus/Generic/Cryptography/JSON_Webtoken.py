import jwt

class JSON_Webtoken:

    def __init__(self):
        self._key = None

    async def encode(self, data):
        return jwt.encode(
            data,
            self.key,
            algorithm = 'HS256'
        ).decode()

    async def decode(self, data):
        return jwt.decode(
            data,
            self.key,
            algorithm = ['HS256']
        )

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key