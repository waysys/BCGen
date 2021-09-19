# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "16-Sep-2021"

"""
This module specifies the Suspense Payment Make Test Case
"""

from models.spec import TestTableSpecification, TestCaseSpecification
from models.paymenthistory import PaymentHistory
from pyodbc import Connection
from queries.policycenterqueries import PolicyCenterQueries
from datetime import datetime
from base.uniqueid import gen_unique_id
from base.testrandom import Random, DEFAULT_SEED

# -------------------------------------------------------------------------------
#  Suspense Payment Make Test Table
# -------------------------------------------------------------------------------


class SuspensePaymentMakeTestTable(TestTableSpecification):
    """
    This class specifies how the suspense payment make test table is formed.
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
        self.heading = "Create suspense payments"
        self.fixture = "castlebay.gfit.billingcenter.SuspensePaymentMakeFixture"
        self.columns = ["TestId",
                        "RefNumber",
                        "Account Number",
                        "Payment Amount",
                        "Comment"]
        self.is_unique = [False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "SUSPENSE-PAYMENT-"
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

        Arguments:
            payment_history - a dictionary of the created payments
        """
        policy_periods = self.pc_queries.query_policy_periods(self.selection_end, self.number_of_rows)
        count = self.test_id_start
        for policy_period in policy_periods:
            row = self.create_row(self.test_id_prefix, count, policy_period)
            self.add_row(row)
            payment_history[row[1]] = PaymentHistory(row[1], row[2], False, False)
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
            self.ref_prefix + str(count),
            policy_period.AccountNumber,
            self.payment_amount,
            "Create suspense payment"
        ]
        return row

# -------------------------------------------------------------------------------
#  Suspense Payment Apply Test Table
# -------------------------------------------------------------------------------


class SuspensePaymentApplyTestTable(TestTableSpecification):
    """
    This class specifies how the suspense payment make test table is formed.
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
        self.heading = "Apply suspense payments"
        self.fixture = "castlebay.gfit.billingcenter.SuspensePaymentModifyFixture"
        self.columns = ["TestId",
                        "RefNumber",
                        "Account Number",
                        "Apply()",
                        "Comment"]
        self.is_unique = [False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "SUSPENSE-APPLY-"
        # the percent of payments to be applies
        self.apply_weight = 20
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

        Arguments:
            payment_history - a dictionary of payments made
        """
        count = self.test_id_start
        for key in payment_history:
            if self.random.select(self.apply_weight):
                payment = payment_history[key]
                row = self.create_row(self.test_id_prefix, count, payment)
                self.add_row(row)
                payment_history[row[1]].applied = True
                count += 1
        return

    @staticmethod
    def create_row(prefix: str, count: int, payment) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
           prefix - the prefix for the test id
           count - the number of the row
           payment - the payment history
        """
        row = [
            prefix + str(count),
            payment.ref_number,
            payment.account_number,
            "true",
            "Apply suspense payment"
        ]
        return row

# -------------------------------------------------------------------------------
#  Suspense Payment Apply Test Table
# -------------------------------------------------------------------------------


class SuspensePaymentReverseTestTable(TestTableSpecification):
    """
    This class specifies how the suspense payment make test table is formed.
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
        self.heading = "Reverse suspense payments"
        self.fixture = "castlebay.gfit.billingcenter.SuspensePaymentModifyFixture"
        self.columns = ["TestId",
                        "RefNumber",
                        "Reverse()",
                        "Comment"]
        self.is_unique = [False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "SUSPENSE-REVERS-"
        # the percent of payments to be reversed
        self.apply_weight = 50
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

        Arguments:
            payment_history - a dictionary of payments made
        """
        count = self.test_id_start
        for key in payment_history:
            payment = payment_history[key]
            if (not payment.applied) and self.random.select(self.apply_weight):
                row = self.create_row(self.test_id_prefix, count, payment)
                self.add_row(row)
                payment_history[row[1]].applied = True
                count += 1
        return

    @staticmethod
    def create_row(prefix: str, count: int, payment) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
           prefix - the prefix for the test id
           count - the number of the row
           payment - the payment history
        """
        row = [
            prefix + str(count),
            payment.ref_number,
            "true",
            "Reverse suspense payment"
        ]
        return row

# -------------------------------------------------------------------------------
#  Invoice Check Test
# -------------------------------------------------------------------------------


class SuspensePaymentMakeTest(TestCaseSpecification):
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
        self.suite_name = "SuspensePaymentMake"
        self.suite_id = "SUSPENSE_PAYMENT_MAKE"
        self.description = \
            """
            This test case creates suspense payments of various amount.  It then generates test that 
            apply some of the payments.  It then generates tests that reverse some of the payments that have not
            been applied.  This test case is a one-time test case.
            New suspense payments should be generated each time an execution of the test case is desired.
            """
        self.version = "2021-09-16"
        self.author = "W. Shaffer"
        self.repeatable = "No"
        #
        # Specify the suspense payments to create
        #
        self.payment_history: dict[str, PaymentHistory] = {}
        table = SuspensePaymentMakeTestTable(cnx)
        table.generate_rows(self.payment_history)
        assert table.has_rows, "No payments were generated"
        self.add_test_table(table)
        #
        # Specify the suspense payments to apply
        #
        table = SuspensePaymentApplyTestTable()
        table.generate_rows(self.payment_history)
        # Add the table only if rows of data were generated
        if table.has_rows:
            self.add_test_table(table)
        #
        # Specify the suspense payments to be reversed
        #
        table = SuspensePaymentReverseTestTable()
        table.generate_rows(self.payment_history)
        # Add the table only if rows of data were generated.
        if table.has_rows:
            self.add_test_table(table)
        return
