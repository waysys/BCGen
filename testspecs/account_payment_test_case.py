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

from datetime import datetime

from pyodbc import Connection

from base.testrandom import Random, DEFAULT_SEED
from base.uniqueid import gen_unique_id
from models.paymenthistory import PaymentHistory
from models.spec import TestTableSpecification, TestCaseSpecification
from queries.policycenterqueries import PolicyCenterQueries


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
        self.number_of_rows = 30
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
            payment_history - the history of payments
        """
        policy_periods = self.pc_queries.query_policy_periods(self.selection_end, self.number_of_rows)
        count = self.test_id_start
        for policy_period in policy_periods:
            row = self.create_row(self.test_id_prefix, count, policy_period)
            self.add_row(row)
            payment_history[row[2]] = PaymentHistory(row[2], row[1], False, False)
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
#  Account Payment Reverse Test Table
# -------------------------------------------------------------------------------


class AccountPaymentReverseTestTable(TestTableSpecification):
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
        self.fixture = "castlebay.gfit.billingcenter.PaymentModifyFixture"
        self.columns = ["TestId",
                        "RefNumber",
                        "Reverse()",
                        "Comment"]
        self.is_unique = [False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "PAYMENT-REVERSE-"
        # the percent of payments to be reversed
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
            payment = payment_history[key]
            if (not payment.reversed) and self.random.select(self.apply_weight):
                row = self.create_row(self.test_id_prefix, count, payment)
                self.add_row(row)
                payment_history[row[1]].reversed = True
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
            "Reverse account payment"
        ]
        return row


# -------------------------------------------------------------------------------
#  Account Disbursement Test Table
# -------------------------------------------------------------------------------


class AccountDisbursementTestTable(TestTableSpecification):
    """
    This class specifies how the account disbursement test table is formed.
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
        self.heading = "Create account disbursements"
        self.fixture = "castlebay.gfit.billingcenter.DisbursementMakeFixture"
        self.columns = ["TestId",
                        "RefNumber",
                        "Account Number",
                        "Payment Amount",
                        "Reason",
                        "Send",
                        "Valid()",
                        "Comment"]
        self.is_unique = [False, False, False, False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "ACCOUNT-DISBURSEMENT-"
        self.ref_prefix = gen_unique_id()
        self.payment_range = (10, 100)
        self.apply_weight = 50
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
            payment_history - a dictionary of payments made
        """
        count = self.test_id_start
        for key in payment_history:
            payment = payment_history[key]
            if (not payment.reversed) and self.random.select(self.apply_weight):
                row = self.create_row(self.test_id_prefix, count, payment)
                self.add_row(row)
                payment.disbursed = True
                count += 1
        return

    def create_row(self, prefix: str, count: int, payment) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
            prefix - the prefix for the test id
            count - the number of the row
            payment - an entry from payment history
        """
        row = [
            prefix + str(count),
            self.ref_prefix + str(count),
            payment.account_number,
            str(self.payment_amount),
            "Overpay",
            "true",
            "true",
            "Create account payment"
        ]
        return row


# -------------------------------------------------------------------------------
#  Account Payment Make Test
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
            This test case creates direct accounts payments of various amount. It then reverses some of
            the payments.  It issues disbursements from accounts that did not have payments. 
            This test case is a one-time test case.
            New payments and disbursements should be generated each time an execution of the test case is desired.
            """
        self.version = "2021-09-20"
        self.author = "W. Shaffer"
        self.repeatable = "No"
        #
        # Specify the account payment table
        #
        self.payment_history: dict[str, PaymentHistory] = {}
        table = AccountPaymentMakeTestTable(cnx)
        table.generate_rows(self.payment_history)
        self.add_test_table(table)
        #
        # Specify the account reversal table
        #
        table = AccountPaymentReverseTestTable()
        table.generate_rows(self.payment_history)
        # Add the table only if rows of data were generated.
        if table.has_rows:
            self.add_test_table(table)
        #
        # Specify account disbursement test table
        #
        table = AccountDisbursementTestTable()
        table.generate_rows(self.payment_history)
        # Add the table only if rows of data were generated.
        if table.has_rows:
            self.add_test_table(table)
        return
