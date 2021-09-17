# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "17-Sep-2021"

"""
This module specifies the Account Payment Make test case.
"""

from models.spec import TestTableSpecification, TestCaseSpecification
from pyodbc import Connection
from queries.policycenterqueries import PolicyCenterQueries
from datetime import datetime
from base.uniqueid import gen_unique_id

# -------------------------------------------------------------------------------
#  Account Payment Make Test Table
# -------------------------------------------------------------------------------


class AccountPaymentMakeTestTable(TestTableSpecification):
    """
    This class specifies how the account payment make test table is formed.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Specify the characteristics of the test table.
        """
        super().__init__()
        self.heading = "Create account direct payments"
        self.fixture = "castlebay.gfit.billingcenter.AccountPaymentMakeFixture"
        self.columns = ["TestId",
                        "Account Number",
                        "RefNumber",
                        "Payment Amount",
                        "Comment"]
        self.is_unique = [False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "ACCOUNT-PAYMENT-"
        self.ref_prefix = gen_unique_id()
        self.payment_range = (100, 1000)
        #
        # Set up query of PolicyCenter
        #
        self.pc_queries = PolicyCenterQueries(cnx)
        self.selection_end = datetime.now()
        self.number_of_rows = 20
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def generate_rows(self):
        """
        Generate the rows for the test table.
        """
        policy_periods = self.pc_queries.query_policy_periods(self.selection_end, self.number_of_rows)
        count = self.test_id_start
        for policy_period in policy_periods:
            row = self.create_row(self.test_id_prefix, count, policy_period)
            self.add_row(row)
            count += 1
        return

    def create_row(self, prefix: str, count: int, policy_period) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
            prefix - the prefix for the test id
            count - the number of the row
            policy_period - a row from the results of a query of the policy period and related data
        """
        row = [
            prefix + str(count),
            policy_period.AccountNumber,
            self.ref_prefix + str(count),
            str(policy_period.TotalInvoicedAmount),
            "Create account payment"
        ]
        return row

# -------------------------------------------------------------------------------
#  Invoice Check Test
# -------------------------------------------------------------------------------


class AccountPaymentMakeTest(TestCaseSpecification):
    """
    This class specifies how the test case for the suspense payment make test case.
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
        self.suite_name = "AccountPaymentMake"
        self.suite_id = "ACCOUNT_PAYMENT_MAKE"
        self.description = \
            """
            This test case creates direct accounts payments of various amount.  This test case is a one-time test case.
            New suspense payments should be generated each time an execution of the test case is desired.
            """
        self.version = "2021-09-17"
        self.author = "W. Shaffer"
        self.repeatable = "No"
        #
        # Specify the tables in the test case
        #
        table = AccountPaymentMakeTestTable(cnx)
        table.generate_rows()
        self.add_test_table(table)
        return