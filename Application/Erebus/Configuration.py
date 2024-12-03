from Erebus.Generic.Accessors.File import File

class Configuration:

    __instance = None

    def __init__(self):
        if Configuration.__instance != None:
            raise Exception("Configuration cannot be initialised more than once.")
        else:
            Configuration.__instance = self

            self._configuration_data = File.read_yaml_file("./Configuration.yml")

    @property
    def configuration_data(self):
        return Configuration.__instance._configuration_data

    @property
    def ssl_cert(self):
        return self.configuration_data["ssl_cert"]

    @property
    def ssl_key(self):
        return self.configuration_data["ssl_key"]

    @property
    def mysql_details(self):
        return self.configuration_data["mysql"]

    @property
    def mongo_details(self):
        return self.configuration_data["mongo"]

    @property
    def redis(self):
        return self.configuration_data["redis"]

    @property
    def application_details(self):
        return self.configuration_data["application"]

    @property
    def jwt_key(self):
        return self.configuration_data["jwt_key"]

    @staticmethod
    def instance():
        if Configuration.__instance == None:
            return Configuration()

        return Configuration.__instance