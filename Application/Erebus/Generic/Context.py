from Generic.Accessors.File import File
from Generic.Storage.Databases.MySQL import MySQL
from Generic.Storage.Databases.Mongo import Mongo
from Generic.Cryptography.JSON_Webtoken import JSON_Webtoken

class Context(File):

    def __init__(self):
        self._file_handle = File()
        self._database = MySQL()
        self._mongo = Mongo()
        self._jwt_controller = JSON_Webtoken()

    @property
    def file_handle(self):
        """An accessor method for the file handler
        instance.

        Returns:
            instance: The file handler instance.
        """
        return self._file_handle

    @property
    def database(self):
        return self._database

    @property
    def mongo(self):
        return self._mongo

    @property
    def jwt_controller(self):
        return self._jwt_controller