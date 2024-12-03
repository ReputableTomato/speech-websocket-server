class Store:

    def __init__(self):
        self._database = {}
        self._account_id = None
        self._data_id = None

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, database):
        self._database = database

    def setup(self, audit_type, data):
        if self.account_id not in self.database:
            self.database[self.account_id] = {}

        if self.data_id not in self.database[self.account_id]:
            self.database[self.account_id][self.data_id] = {}

        if "paths" not in self.database[self.account_id][self.data_id]:
            self.database[self.account_id][self.data_id]["paths"] = {}

        if "timestamp" not in self.database[self.account_id][self.data_id]:
            self.database[self.account_id][self.data_id]["timestamp"] = int(float(data["timestamp"]))

    def add(self, audit_type, data):
        self.setup(audit_type, data)
        self.database[self.account_id][self.data_id][audit_type] = data

    def path(self, audit_type, data):
        self.setup(audit_type, data)

        paths = self.database[self.account_id][self.data_id]["paths"]

        if not paths:
            path_index = str("1")
        else:
            path_index = str(len(paths) + 1)

        self.database[self.account_id][self.data_id]["paths"][path_index] = data

    def get(self):
        return self.database[self.account_id][self.data_id]

    def exists(self):
        if self.account_id not in self.database:
            return False

        if self.account_id not in self.database[self.account_id]:
            return False

        return True

    def all(self):
        return self.database

    @property
    def data_id(self):
        return self._data_id

    @data_id.setter
    def data_id(self, data_id):
        self._data_id = data_id

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id