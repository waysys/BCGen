# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "01-Sep-2021"

"""
This module executes a SQL query and manages the error handling.
"""

from base.testexception import TestException


# -------------------------------------------------------------------------------
#  Manage a query
# -------------------------------------------------------------------------------


class Query:
    """
    Manage a query.  Execute the query and manage the error handling.  Return a
    result of all the returned values.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx):
        """
        Initialize the instance of a class.

        Argument:
            cnx - a connection to a database
        """
        assert cnx is not None, "Connection for query must not be null"
        self._cnx = cnx
        return

    # -------------------------------------------------------------------------------
    # Operations
    # -------------------------------------------------------------------------------

    def query(self, statement, *argv):
        """
        Perform a SQL query against the database that this class is connected to.
        Return a list of results.

        Arguments:
            statement - an SQL select statement
            argv - a variable number of arguments for the SQL statement
        """
        assert statement is not None, "The query statement must not be null"
        assert len(statement) > 0, "The query string cannot be an empty string"
        cursor = self._cnx.cursor()
        results = None
        try:
            cursor.execute(statement, argv)
            results = cursor.fetchall()
        except Exception as e:
            message = "Error in query: " + str(e)
            print(message)
            raise TestException(message)
        finally:
            try:
                cursor.close()
            except Exception as e:
                print("Error in closing cursor: " + str(e))
        return results

    def execute(self, statement, *argv):
        """
        Execute a stored procedure.  When querying a stored procedure in SQL Server,
        the DBMS returns multiple result sets.  The first result set contains the current
        date.  The second result set contains the desired data.

        Arguments:
            statement - an SQL select statement
            argv - a variable number of arguments for the SQL statement
        """
        assert statement is not None, "The query statement must not be null"
        assert len(statement) > 0, "The query string cannot be an empty string"
        cursor = self._cnx.cursor()
        results = None
        try:
            cursor.execute(statement, argv)
            # if cursor.nextset():
            results = cursor.fetchall()
            # else:
            # raise TestException("There was only one result set from query: " + statement)
        except Exception as e:
            message = "Error in query: " + str(e)
            print(message)
            raise TestException(message)
        finally:
            try:
                cursor.close()
            except Exception as e:
                print("Error in closing cursor: " + str(e))
        return results

    def delete(self, statement, *argv):
        """
        Execute a delete statement.

        Arguments:
            statement - the SQL DELETE statement
            argv - any arguments to the statement
        """
        assert statement is not None, "The delete statement must not be null"
        assert len(statement) > 0, "The delete statement cannot be an empty string"
        cursor = self._cnx.cursor()
        try:
            cursor.execute(statement, argv)
            cursor.commit()
        except Exception as e:
            message = "Error in query: " + str(e)
            print(message)
            raise TestException(message)
        finally:
            try:
                cursor.close()
            except Exception as e:
                print("Error in closing cursor: " + str(e))
        return

    def insert(self, statement):
        """
        Insert a single row of data into the database.

        Arguments:
            statement - the SQL INSERT statement with the data defined.
        """
        assert statement is not None, "The insert statement must not be null"
        assert len(statement) > 0, "The insert statement cannot be an empty string"
        cursor = self._cnx.cursor()
        try:
            cursor.execute(statement)
            cursor.commit()
        except Exception as e:
            message = "Error in insert: " + str(e)
            print(message)
            raise TestException(message)
        finally:
            try:
                cursor.close()
            except Exception as e:
                print("Error in closing cursor: " + str(e))
        return

    def update(self, statement):
        """
        Update one or more rows of data in the database.

        Arguments:
            statement - the SQL UPDATE statement with the data defined.
        """
        assert statement is not None, "The insert statement must not be null"
        assert len(statement) > 0, "The insert statement cannot be an empty string"
        cursor = self._cnx.cursor()
        try:
            cursor.execute(statement)
            cursor.commit()
        except Exception as e:
            message = "Error in update: " + str(e)
            print(message)
            raise TestException(message)
        finally:
            try:
                cursor.close()
            except Exception as e:
                print("Error in closing cursor: " + str(e))
        return
