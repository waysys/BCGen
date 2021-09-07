# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------


__author__ = 'Bill Shaffer'
__version__ = "01-Sep-2021"

"""
This module manages a connection to SQL Server
"""

import pyodbc
from string import Template

# -------------------------------------------------------------------------------
# Connector class for SQL Server Authentication
# -------------------------------------------------------------------------------


class Connector:
    """
    This class manages a connection to a SQL SERVER database.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize the class
        """
        self._driver = '{ODBC Driver 17 for SQL Server}'
        self._server = None
        self._database = None
        self._username = None
        self._password = None
        return

    # -------------------------------------------------------------------------------
    # Properties
    # -------------------------------------------------------------------------------

    @property
    def driver(self):
        """
        Return the string that identifies the SQL Server driver
        """
        return self._driver

    @property
    def server(self):
        """
        Return the name of the server containing the database.
        """
        assert self._server is not None, "Server has not been set"
        return self._server

    @server.setter
    def server(self, value):
        assert value is not None, "Server must not be None"
        assert len(value) > 0, "Server name must not be empty"
        self._server = value
        return

    @property
    def database(self):
        """
        Return the name of the database
        """
        assert self._database is not None, "Database name has not been set"
        return self._database

    @database.setter
    def database(self, value):
        """
        Set the name of the database
        """
        assert value is not None, "Database name must not be None"
        assert len(value) > 0, "Database name must not be empty"
        self._database = value
        return

    @property
    def username(self):
        """
        Return the user name for accessing the database.
        """
        assert self._username is not None, "User name has not been set"
        return self._username

    @username.setter
    def username(self, value):
        """
        Set the user name for access to the database.

        Argument:
            value - the new user name
        """
        assert value is not None, "User name must not be None"
        assert len(value) > 0, "User name must not be empty"
        self._username = value
        return

    @property
    def password(self):
        """
        Return the password associated with the user name.
        """
        assert self._password is not None, "Password must not be None"
        return self._password

    @password.setter
    def password(self, value):
        """
        Set the password to value
        """
        assert value is not None, "Password must not be None"
        assert len(value) > 0, "Password must not be empty"
        self._password = value
        return

    # -------------------------------------------------------------------------------
    # Operations
    # -------------------------------------------------------------------------------

    def connect(self) -> pyodbc.Connection:
        """
        Connect to a SQL Server database and return the connection.
        """
        connection_string = self.build_connection_string()
        cnx = pyodbc.connect(connection_string)
        return cnx

    def build_connection_string(self):
        """
        Return a connection string based on the properties in this class.
        """
        template = Template("DRIVER=$DRIVER;SERVER=$SERVER;DATABASE=$DATABASE;UID=$USERNAME;PWD=$PASSWORD")
        connection_string = template.substitute(DRIVER=self.driver,
                                                SERVER=self.server,
                                                DATABASE=self.database,
                                                USERNAME=self.username,
                                                PASSWORD=self.password)
        return connection_string

    @staticmethod
    def create_connector(server: str, database: str) -> pyodbc.Connection:
        """
        Create and return a connector to the database with the parameters from the environment.

        Argument:
            environ - the code for the environment
        """
        assert server is not None, "Server name must not be None"
        assert len(server) > 0, "Server name must not be empty"
        assert database is not None, "Database name must not be None"
        assert len(database) > 0, "Database name must not be empty"
        connector = ConnectorWindows()
        connector.dsn = server
        connector.database = database
        cnx = connector.connect()
        return cnx

# -------------------------------------------------------------------------------
# Connector class for SQL Server Authentication
# -------------------------------------------------------------------------------


class ConnectorWindows(Connector):
    """
    This class creates a connector based on a Windows ODBC data source.  This
    type of connector should be used when Windows authentication is required.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize the class.
        """
        super().__init__()
        self._dsn = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def dsn(self):
        """
        The name of the ODBC data source.  This data source must already
        be set up using the Windows control panel.
        """
        assert self._dsn is not None, "DSN has not been set yet"
        return self._dsn

    @dsn.setter
    def dsn(self, name):
        """
        Set the value of the data source name.

        Argument:
            name - the name of the data source
        """
        assert name is not None, "DSN must not be None"
        assert len(name) > 0, "DSN must not be an empty string"
        self._dsn = name
        return

    # -------------------------------------------------------------------------------
    # Operations
    # -------------------------------------------------------------------------------

    def build_connection_string(self):
        """
        Return the connection string for the connector.
        """
        template = Template("DSN=$DSN;DATABASE=$DATABASE;Trusted_Connection=yes;")
        connection_string = template.substitute(DSN=self.dsn, DATABASE=self.database)
        return connection_string
