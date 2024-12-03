import os
import json

from Erebus.Generic.Accessors.File import File
from Erebus.Generic.Storage.Databases.MySQL import MySQL
from Erebus.Generic.Cryptography.JSON_Webtoken import JSON_Webtoken
from Erebus.Generic.Storage.Memory.Store import Store
from Erebus.Networking.Constants import Constants
from Erebus.Configuration import Configuration
from Erebus.Networking.Websockets.WebsocketConnectionHandler import WebsocketConnectionHandler

class Context:

    __instance = None

    def __init__(self):

        if Context.__instance == None:
            Context.__instance = self

            self.__file_handle = File()
            self.__database = MySQL()
            self.__jwt_controller = JSON_Webtoken()

            self.__configuration = Configuration()
            self.__connection_handler = WebsocketConnectionHandler()
            self.__root_path = self.file_handle.basename(os.path.realpath(__file__)) + "../"
            self.__database_store = Store()
            self.__jwt_controller.key = self.configuration.jwt_key
            self.__constants = Constants()

            self.database_setup()

    @property
    def root_path(self):
        return self.instance().__root_path

    @property
    def file_handle(self):
        return self.instance().__file_handle

    @property
    def database(self):
        return self.instance().__database

    @property
    def jwt_controller(self):
        return self.instance().__jwt_controller

    @property
    def configuration(self):
        return self.instance().__configuration

    @property
    def connection_handler(self):
        return self.instance().__connection_handler

    @property
    def database_store(self):
        return self.instance().__database_store

    @property
    def constants(self):
        return self.instance().__constants

    def database_setup(self):
        self.database.set_credentials(
            host = self.configuration.mysql_details["host"],
            database_name = self.configuration.mysql_details["database_name"],
            user = self.configuration.mysql_details["user"],
            password = self.configuration.mysql_details["password"],
        )

    @staticmethod
    def instance():
        if __class__.__instance == None:
            return __class__()

        return __class__.__instance