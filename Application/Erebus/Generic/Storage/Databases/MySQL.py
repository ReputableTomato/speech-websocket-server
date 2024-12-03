import mysql.connector

class MySQL:

    def __init__(self):
        self._connection = None
        self._cursor = None
        self._query = None
        self._binds = ()
        self._host = None
        self._database_name = None
        self._user = None
        self._password = None
        self._last_id = None

    def set_credentials(self, host, database_name, user, password):
        self.host = host
        self.database_name = database_name
        self.user = user
        self.password = password

    def connect(self):
        """A method to connect to a MySQL database. This
        function is automatically set to use prepared
        statements.

        Args:
            host (string): The database hostname.
            database_name (string): The database name.
            user (string): The datbase username.
            password (string): The database password.
        """
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                database = self.database_name,
                user = self.user,
                password = self.password,
                # We use the native mysql password authentication method
                auth_plugin = 'mysql_native_password'
            )
        except mysql.connector.Error as error:
            raise mysql.connector.Error("Could not setup a database connection: {}".format(error))

    def disconnect(self):
        self.connection.close()

    def execute(self):
        """ A method to execute a query that has been set."""
        self.connect()
        self.cursor = self.connection.cursor(
            prepared = True
        )

        self.cursor.execute(
            self.query,
            self.binds
        )
        self.connection.commit()
        self.last_id = self.cursor.lastrowid

        self.cursor.close()
        self.disconnect()

        return self.last_id

    def single(self):
        """Executes a set query and returns a single row.

        Returns:
            dict: The data returns from the query.
        """
        self.connect()
        self.cursor = self.connection.cursor(
            prepared = True
        )

        self.cursor.execute(
            self.query,
            self.binds
        )

        results = self.cursor.fetchone()

        if results:
            # We do this so that we can replace the value by the index.
            results = list(results)

            for index, item in enumerate(results):
                # If the value is a bytearray, we convert it to a string.
                if isinstance(item, bytearray):
                    results[index] = item.decode()

            # We combine the columns with the results.
            results = dict(zip(self.cursor.column_names, results))

        self.cursor.close()
        self.disconnect()

        return results

    def resultset(self):
        """Executes a set query and returns all the rows.

        Returns:
            dict: The data returns from the query.
        """
        self.connect()
        self.cursor = self.connection.cursor(
            prepared = True
        )

        self.cursor.execute(
            self.query,
            self.binds
        )

        results = self.cursor.fetchall()

        if results:
            # We turn our data into a list(key/value) structure.
            columns = [col[0] for col in self.cursor.description]
            results = [dict(zip(columns, row)) for row in results]

            # We need to decode any bytearray values we may have.
            for row_index, row in enumerate(results):
                for column_key in row:
                    if isinstance(row[column_key], bytearray):
                        row[column_key] = row[column_key].decode()

        self.cursor.close()
        self.disconnect()

        return results

    @property
    def binds(self):
        """An accessor method for the binds.
        
        Returns:
            tuple: The binds.
        """
        return self._binds

    @binds.setter
    def binds(self, binds):
        """A method to set the binds for an sql query.
        
        Args:
            binds (list): The binds.
        """
        self._binds = tuple(binds)

    @property
    def query(self):
        """An accessor method for the set sql query.
        
        Returns:
            string: The sql query.
        """
        return self._query

    @query.setter
    def query(self, query):
        """A method to set an sql query.
        
        Args:
            query (string): The sql query.
        """
        self._query = query

    @property
    def connection(self):
        """An accessor method for the current database connection.
        
        Returns:
            MySQLConnection: The database connection.
        """
        return self._connection

    @connection.setter
    def connection(self, connection):
        """A method to set the database connection.
        
        Args:
            connection (MySQLConnection): The database connection.
        """
        self._connection = connection

    @property
    def cursor(self):
        """An accessor method for the database cursor.
        
        Returns:
            MySQLCursorPrepared: The database cursor.
        """
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        """A method to set the database cursor.
        
        Args:
            cursor (MySQLCursorPrepared): The database cursor.
        """
        self._cursor = cursor

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
    def last_id(self):
        return self._last_id

    @last_id.setter
    def last_id(self, last_id):
        self._last_id = last_id