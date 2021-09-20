# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "18-Sep-2021"

"""
This class specifies the Payment Make test case for creating policy-level payments.
"""

from datetime import datetime

from pyodbc import Connection

from base.testrandom import Random, DEFAULT_SEED
from base.uniqueid import gen_unique_id
from models.spec import TestTableSpecification, TestCaseSpecification
from models.paymenthistory import PaymentHistory
from queries.policycenterqueries import PolicyCenterQueries


# -------------------------------------------------------------------------------
#  Payment Make Test Table
# -------------------------------------------------------------------------------


class PaymentMakeTestTable(TestTableSpecification):
    """
    This class specifies how the payment make test table is formed.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Specify the characteristics of the test table.
        """
        super().__init__()
        self.heading = "Create direct policy payments"
        self.fixture = "castlebay.gfit.billingcenter.PaymentMakeFixture"
        self.columns = ["TestId",
                        "Account Number",
                        "Policy Number",
                        "RefNumber",
                        "Payment Amount",
                        "Comment"]
        self.is_unique = [False, False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "POLICY-PAYMENT-"
        self.ref_prefix = gen_unique_id()
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

    def generate_rows(self, payment_history: dict[str, PaymentHistory]):
        """
        Generate the rows for the test table.
        """
        policy_periods = self.pc_queries.query_policy_periods(self.selection_end, self.number_of_rows)
        count = self.test_id_start
        for policy_period in policy_periods:
            if self.is_in_effect(policy_period, self.selection_end):
                row = self.create_row(self.test_id_prefix, count, policy_period)
                self.add_row(row)
                payment_history[row[3]] = PaymentHistory(row[3], policy_period.AccountNumber, False, False)
                payment_history[row[3]].policy_number = policy_period.PolicyNumber
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
            policy_period.AccountNumber,
            policy_period.PolicyNumber,
            self.ref_prefix + str(count),
            str(policy_period.TotalInvoicedAmount),
            "Create account payment"
        ]
        return row

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

    def __init__(self):
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
        self.apply_weight = 90
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

    def generate_rows(self, payment_history: dict[str, PaymentHistory]):
        """
        Generate the rows for the test table.
        """
        count = self.test_id_start
        for key in payment_history:
            payment = payment_history[key]
            if self.random.select(self.apply_weight):
                row = self.create_row(self.test_id_prefix, count, payment)
                self.add_row(row)
                count += 1
        return

    def create_row(self, prefix: str, count: int, payment: PaymentHistory) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
            prefix - the prefix for the test id
            count - the number of the row
            policy_period - a row from the results of a query of the policy period and related data
        """
        row = [
            prefix + str(count),
            "negative write-off",
            payment.account_number,
            payment.policy_number,
            str(self.payment_amount),
            "miscellaneous",
            "true",
            "Create negative write-off"
        ]
        return row


# -------------------------------------------------------------------------------
#  Payment Make Test
# -------------------------------------------------------------------------------


class PaymentMakeTest(TestCaseSpecification):
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
        self.suite_name = "PaymentMake"
        self.suite_id = "PAYMENT_MAKE"
        self.description = \
            """
            This test case creates direct payments of various amount for policies.  This test case is a one-time 
            test case.  New suspense payments should be generated each time an execution of the test case is desired.
            """
        self.version = "2021-09-18"
        self.author = "W. Shaffer"
        self.repeatable = "No"
        #
        # Create payment on policy
        #
        self.payment_history: dict[str, PaymentHistory] = {}
        table = PaymentMakeTestTable(cnx)
        table.generate_rows(self.payment_history)
        self.add_test_table(table)
        #
        # Specify negative write-offs
        #
        table = WriteOffMakeTestTable()
        table.generate_rows(self.payment_history)
        if table.has_rows:
            self.add_test_table(table)
        return
