# -------------------------------------------------------------------------------
#
#  Copyright (c) 2019 Franklin Mutual Insurance
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "14-Oct-2019"

"""
This module tests the Connector class.
"""

from base.connector import Connector, ConnectorWindows
from queries.claimcenterqueries import ClaimCenterQuery
import unittest
import xmlrunner


# -------------------------------------------------------------------------------
# Test of the Connector class
# -------------------------------------------------------------------------------


class TestConnector(unittest.TestCase):
    """
    Test the ability to connect to the DataHub database.
    """
    def setUp(self):
        """
        Initialize the connector.
        """
        self.connector = Connector()
        self.connector.server = "GWDEVDSV10"
        self.connector.database = "DH_DEV"
        self.connector.username = "bshaffer"
        self.connector.password = "DEVgwFMI2019"
        return

    def test_01_connect_string(self):
        """
        Test that the connection string is built properly.
        """
        connection_string = self.connector.build_connection_string()
        print(connection_string)
        return

    def test_02_database_connection(self):
        """
        Test that the connector actually connects to the database.
        """
        cnx = self.connector.connect()
        cursor = cnx.cursor()
        self.assertEqual(-1, cursor.rowcount, "Cursor did not return -1")
        return

    def test_03_database_connection_with_odbc_datasource(self):
        """
        Test connection through ODB data source.
        """
        self.connector = ConnectorWindows()
        self.connector.dsn = "QA"
        self.connector.database = "GWCC"
        cnx = self.connector.connect()
        cursor = cnx.cursor()
        self.assertEqual(-1, cursor.rowcount, "Cursor did not return -1")
        query = ClaimCenterQuery(cnx)
        count = query.query_policy_count()
        self.assertTrue(count > 0, "Policy count was not returned: " + str(count))
        return


if __name__ == '__main__':
    report_file = 'C:/GFITWorkspaces/DH/GLtest.xml'
    with open(report_file, 'wb') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
