import bcrypt

from Erebus.Context import Context
from Erebus.Networking.UserTypes.IAccount import IAccount

class UserAccount(IAccount):

    def __init__(self):
        self._id = None
        self._username = None
        self._email = None
        self._password_hash = None
        self._ip_address = None
        self._status = None
        self._groups = []

    def get(self, username = None, id = None) -> dict:
        if username:
            self.database.query = "SELECT id, username, email, password_hash, ip_address, status FROM user WHERE username = %s;"
            self.database.binds = [username]

        if id:
            self.database.query = "SELECT id, username, email, password_hash, ip_address, status FROM user WHERE id = %s;"
            self.database.binds = [id]

        account = self.database.single()

        # Set the account data if it exists.
        self.id = account["id"]
        self.username = account["username"]
        self.email = account["email"]
        self.password_hash = account["password_hash"]
        self.ip_address = account["ip_address"]
        self.status = account["status"]

        # We gather up the groups the user is in after getting the account info.
        self.database.query = """SELECT user_groups.id, name, level FROM user_groups
            JOIN user_permissions ON (user_permissions.group_id = user_groups.id)
            WHERE user_permissions.user_id = %s;"""
        self.database.binds = [self.id]

        self.groups = self.database.resultset()

        return account

    async def create(self, username, email_address, password_hash, ip_address, status):
        self.database.query = "INSERT INTO user (username, email, password_hash, ip_address, status) VALUES (%s, %s, %s, %s, %s);"
        self.database.binds = [username, email_address, password_hash, ip_address, status]
        self.database.execute()

    def remove(self, username):
        pass

    def update(self):
        self.database.query = "UPDATE user SET username = %s, email = %s, password_hash = %s, ip_address = %s, status = %s WHERE id = %s"
        self.database.binds = [
            self.username,
            self.email,
            self.password_hash,
            self.ip_address,
            self.status,
            self.id
        ]
        self.database.execute()

    def exists(self, username = None, email = None):
        if username:
            self.database.query = "SELECT count(id) as count FROM user WHERE username = %s;"
            self.database.binds = [username]
        else:
            self.database.query = "SELECT count(id) as count FROM user WHERE email = %s;"
            self.database.binds = [email]

        result = self.database.single()

        return True if result["count"] else False

    async def verify_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    async def generate_password_hash(self, password):
        salt = bcrypt.gensalt(rounds = 8)

        return bcrypt.hashpw(password.encode(), salt).decode()

    async def add_group(self, user_id, group_id):
        self.database.query = "INSERT INTO user_permissions (user_id, group_id) VALUES (%s, %s);"
        self.database.binds = [user_id, group_id]
        self.database.execute()

    async def add_confirmation(self, user_id, confirmation_code, confirmation_type):
        self.database.query = "INSERT INTO email_confirmation (user_id, confirmation_code, type) VALUES (%s, %s, %s);"
        self.database.binds = [user_id, confirmation_code, confirmation_type]
        self.database.execute()

    async def delete_confirmation(self, confirmation_id):
        self.database.query = "DELETE FROM email_confirmation WHERE id = %s"
        self.database.binds = [confirmation_id]
        self.database.execute()

    async def get_confirmation_code(self, confirmation_code):
        self.database.query = "SELECT id, user_id, confirmation_code, type FROM email_confirmation WHERE confirmation_code = %s;"
        self.database.binds = [confirmation_code]

        return self.database.single()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password_hash):
        self._password_hash = password_hash

    @property
    def ip_address(self):
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address):
        self._ip_address = ip_address

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def groups(self):
        return self._groups

    @groups.setter
    def groups(self, groups):
        self._groups = groups

    def highest_group_level(self):
        highest_level = -1

        if self.groups:
            for group in self.groups:
                if group["level"] > highest_level:
                    highest_level = group["level"]

        return highest_level

    @property
    def nodes(self):
        self.database.query = "SELECT id, owner_id, identifier FROM node WHERE owner_id = %s"
        self.database.binds = [self.id]

        nodes = self.database.resultset()

        return nodes

    @property
    def node_ids(self):
        self.database.query = "SELECT id FROM node WHERE owner_id = %s"
        self.database.binds = [self.id]

        nodes = self.database.resultset()
        node_ids = []

        for node in nodes:
            node_ids.append(node["id"])

        return node_ids

    @property
    def database(self):
        return Context().database