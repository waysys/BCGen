# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "01-Sep-2021"

"""
This module specifies the Account Check Test case
"""

from models.spec import TestTableSpecification, TestCaseSpecification
from queries.policycenterqueries import PolicyCenterQueries
from pyodbc import Connection
from datetime import datetime

# -------------------------------------------------------------------------------
#  Account Check Test Table
# -------------------------------------------------------------------------------


class AccountCheckTestTable(TestTableSpecification):
    """
    This class specifies how the test table for the account check test case is formed.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Specify the characteristics of the test table.
        """
        super().__init__()
        self.heading = "Check that accounts exist"
        self.fixture = "castlebay.gfit.billingcenter.AccountCheckFixture"
        self.columns = ["TestId", "Account Number", "Comment"]
        self.test_id_start = 10
        self.test_id_prefix = "ACCT-CHECK-"
        return


# -------------------------------------------------------------------------------
#  Account Check Test
# -------------------------------------------------------------------------------


class AccountCheckTest(TestCaseSpecification):
    """
    This class specifies how the test case for the Account Check test case.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Initialize the instance of this class with the values for the Account
        Check test case.
        """
        assert cnx is not None, "connection must not be None"
        super().__init__()
        self.project_name = "BillingCenterProject"
        self.suite_name = "AccountCheck"
        self.description = "This test case checks that BillingCenter has the specified accounts from PolicyCenter."
        self.version = "2021-09-03"
        self.author = "W. Shaffer"
        self.test_case_number = "1000"
        #
        # Set up query of PolicyCenter
        #
        self.pc_queries = PolicyCenterQueries(cnx)
        self.selection_start = datetime(2021, 9, 1)
        self.selection_end = datetime(2021, 9, 3)
        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def generate_rows(self):
        """
        Generate the rows for the test table.
        """
        table = AccountCheckTestTable()
        accounts = self.pc_queries.query_accounts(self.selection_start, self.selection_end)
        count = table.test_id_start
        for account in accounts:
            row = self.create_row(table.test_id_prefix, count, account)
            table.add_row(row)
            count += 1
        return

    @staticmethod
    def create_row(prefix: str, count: int, account) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
            account - a row from a query of the account table in PolicyCenter
        """
        row = []
        test_id = prefix + str(count)
        row.append(test_id)
        row.append(account.AccountNumber)
        row.append("Check account " + account.AccountNumber)
        return row

