# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "19-Sep-2021"

"""
This module specifies the Advanced Commission test case.
"""

from models.spec import TestTableSpecification, TestCaseSpecification
from pyodbc import Connection
from queries.policycenterqueries import PolicyCenterQueries
from base.testrandom import Random, DEFAULT_SEED
from base.uniqueid import gen_unique_id

# -------------------------------------------------------------------------------
#  Account Payment Make Test Table
# -------------------------------------------------------------------------------


class AdvancedCommissionTestTable(TestTableSpecification):
    """
    This class specifies how the advanced commissioin payment test table is formed.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Specify the characteristics of the test table.
        """
        super().__init__()
        self.heading = "Create advanced commisson payments"
        self.fixture = "castlebay.gfit.billingcenter.AdvanceCommissionPaymentFixture"
        self.columns = ["TestId",
                        "ProducerCode",
                        "PublicID",
                        "Payment Amount",
                        "Valid()",
                        "Comment"]
        self.is_unique = [False, False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "ADVANCED-COMMISSION-"
        self.ref_prefix = gen_unique_id()
        self.payment_range = (100, 1000)
        self.random = Random(DEFAULT_SEED)
        self.producer_weight = 50
        self.payment_range = (10, 1000)
        #
        # Set up query of PolicyCenter
        #
        self.pc_queries = PolicyCenterQueries(cnx)
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
        producer_codes = self.pc_queries.query_producer_code()
        count = self.test_id_start
        for producer_code in producer_codes:
            if self.random.select(self.producer_weight):
                row = self.create_row(self.test_id_prefix, count, producer_code)
                self.add_row(row)
                count += 1
        return

    def create_row(self, prefix: str, count: int, producer_code) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
            prefix - the prefix for the test id
            count - the number of the row
            policy_period - a row from the results of a query of the policy period and related data
        """
        row = [
            prefix + str(count),
            producer_code.ProducerCode,
            self.ref_prefix + str(count),
            str(self.random.get_random(self.payment_range)),
            "true",
            "Create advanced premium payment"
        ]
        return row

# -------------------------------------------------------------------------------
#  Invoice Check Test
# -------------------------------------------------------------------------------


class AdvancedCommissionTest(TestCaseSpecification):
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
        self.suite_name = "AdvancedCommissionPayment"
        self.suite_id = "ADVANCED_COMMISSION_PAYMENT"
        self.description = \
            """
            This test case creates advanced commmisson payments to a randomly selected list of
            producers.
            """
        self.version = "2021-09-19"
        self.author = "W. Shaffer"
        self.repeatable = "No"
        #
        # Specify the tables in the test case
        #
        table = AdvancedCommissionTestTable(cnx)
        table.generate_rows()
        self.add_test_table(table)
        return
