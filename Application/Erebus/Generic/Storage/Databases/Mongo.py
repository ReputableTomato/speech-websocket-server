from pymongo import MongoClient

class Mongo:

    def __init__(self):
        self._client = None
        self._host = None
        self._username = None
        self._password = None
        self._port = None
        self._database_name = None

    def set_credentials(self, host, port, database_name, user, password):
        self.host = host
        self.port = port
        self.database_name = database_name
        self.user = user
        self.password = password

    def connect(self):
        self.client = MongoClient("mongodb://{}:{}@{}:{}/?authSource={}".format(
            self.user,
            self.password,
            self.host,
            self.port,
            self.database_name
        ))

    @property
    def client(self):
        """An accessor method for the current database client.
        
        Returns:
            Client: The database client.
        """
        return self._client

    @client.setter
    def client(self, client):
        """A method to set the database client.
        
        Args:
            client: The database client.
        """
        self._client = client

    async def find(self, collection_name, json, start = 0, limit = 25):
        if hasattr(self.database, collection_name):
            collection = getattr(self.database, collection_name)
            results = []

            response = collection.find(json).skip(start).limit(limit)

            for result in response:
                results.append(str(result))

            return results
        else:
            raise Exception("{} Collection does not exist.".format(collection_name))

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port):
        self._port = port

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, host):
        self._host = host

    @property
    def database_name(self):
        return self._database_name

    @database_name.setter
    def database_name(self, database_name):
        self._database_name = database_name

    @property
    def database(self):
        return self.client[self.database_name]