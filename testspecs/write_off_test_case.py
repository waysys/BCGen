# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "20-Sep-2021"

"""
This module specifies the Write-Off Test Case.
"""

from datetime import datetime

from pyodbc import Connection

from base.testrandom import Random, DEFAULT_SEED
from base.uniqueid import gen_unique_id
from models.spec import TestTableSpecification, TestCaseSpecification
from queries.policycenterqueries import PolicyCenterQueries


# -------------------------------------------------------------------------------
#  Write-Off Make Test Table
# -------------------------------------------------------------------------------


class WriteOffMakeTestTable(TestTableSpecification):
    """
    This class specifies how the write-off make test table is formed.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Specify the characteristics of the test table.
        """
        super().__init__()
        self.random = Random(DEFAULT_SEED)
        self.heading = "Create write-offs"
        self.fixture = "castlebay.gfit.billingcenter.WriteOffMakeFixture"
        self.columns = ["TestId",
                        "WriteoffType",
                        "Account Number",
                        "Policy Number",
                        "Amount",
                        "Reason",
                        "Valid()",
                        "Comment"]
        self.is_unique = [False, False, False, False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "WRITE-OFF-"
        self.ref_prefix = gen_unique_id()
        self.payment_range = (1, 5)
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

    @property
    def payment_amount(self) -> str:
        """
        Return a random payment amount in dollars.
        """
        return self.random.get_random(self.payment_range)

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
            if self.is_in_effect(policy_period, self.selection_end):
                row = self.create_row(self.test_id_prefix, count, policy_period)
                self.add_row(row)
                count += 1
        return

    @staticmethod
    def is_in_effect(policy_period, date: datetime) -> bool:
        """
        Return True if the policy period is in effect on the specified date.

        Arguments:
            policy_period - a row from the results of a query of the policy period and related data
            date - the date specified for testing
        """
        result = True
        if date < policy_period.PeriodStart:
            result = False
        elif date >= policy_period.PeriodEnd:
            result = False
        return result

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
            "write-off",
            policy_period.AccountNumber,
            policy_period.PolicyNumber,
            str(self.payment_amount),
            "miscellaneous",
            "true",
            "Create account payment"
        ]
        return row


# -------------------------------------------------------------------------------
#  Payment Make Test
# -------------------------------------------------------------------------------


class WriteOffMakeTest(TestCaseSpecification):
    """
    This class specifies how the test case for the write-off make test case.
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
        self.suite_name = "WriteOffMake"
        self.suite_id = "WRITE-OFF"
        self.description = \
            """
            This test case creates write-offs from policies.  This test case is a one-time 
            test case.  New write-offs should be generated each time an execution of the test case is desired.
            """
        self.version = "2021-09-20"
        self.author = "W. Shaffer"
        self.repeatable = "No"
        #
        # Specify the tables in the test case
        #
        table = WriteOffMakeTestTable(cnx)
        table.generate_rows()
        self.add_test_table(table)
        return
