# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "2021-09-02"

"""
This module tests the Connector class.
"""

import unittest
from datetime import datetime

import xmlrunner

from base.connector import Connector
from configuration.config import ConnectorTestConfiguration
from queries.policycenterqueries import PolicyCenterQueries


# -------------------------------------------------------------------------------
# Test of the Connector class
# -------------------------------------------------------------------------------


class TestConnector(unittest.TestCase):
    """
    Test the ability to connect to the DataHub database.
    """

    # -------------------------------------------------------------------------------
    #  Class Variables
    # -------------------------------------------------------------------------------

    configuration = ConnectorTestConfiguration()

    # -------------------------------------------------------------------------------
    #  Support Methods
    # -------------------------------------------------------------------------------

    def setUp(self):
        """
        Initialize the connector.
        """
        self.cnx = Connector.create_connector(self.configuration.data_source)
        return

    def tearDown(self):
        self.cnx.close()
        return

    # -------------------------------------------------------------------------------
    #  Tests
    # -------------------------------------------------------------------------------

    def test_02_database_connection(self):
        """
        Test that the connector actually connects to the database.
        """
        cursor = self.cnx.cursor()
        self.assertEqual(-1, cursor.rowcount, "Cursor did not return -1")
        return

    def test_03_database_connection_with_odbc_datasource(self):
        """
        Test connection through ODB data source.  Perform a query.
        """
        pc_queries = PolicyCenterQueries(self.cnx)
        selection_start = datetime(2021, 9, 1)
        selection_end = datetime(2021, 9, 3)
        results = pc_queries.query_accounts(selection_start, selection_end)
        count = len(results)
        self.assertTrue(count > 0, "Accounts were not found: " + str(count))
        return


if __name__ == '__main__':
    report_file = TestConnector.configuration.report_file
    with open(report_file, 'w') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
