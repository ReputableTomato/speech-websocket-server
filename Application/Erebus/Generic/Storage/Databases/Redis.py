import redis

class Redis:

    def __init__(self, host, port, password, database, decode_responses = True):
        self.__connection = None
        self.__host = host
        self.__port = port
        self.__database = database
        self.__password = password
        self.__decode_responses = decode_responses

    def connect(self):
        self.connection = redis.Redis(
            host = self.host,
            port = self.port,
            db = self.database,
            password = self.password,
            decode_responses = self.decode_responses
        )

        return self.connection

    @property
    def connection(self):
        return self.__connection

    @connection.setter
    def connection(self, connection):
        self.__connection = connection

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def database(self):
        return self.__database

    @database.setter
    def database(self, database):
        self.__database = database

    @property
    def decode_responses(self):
        return self.__decode_responses

    @decode_responses.setter
    def decode_responses(self, decode_responses):
        self.__decode_responses = decode_responses