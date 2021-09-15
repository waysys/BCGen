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
from models.policyperiod import PolicyPeriod, PolicyStatus
from queries.policycenterqueries import PolicyCenterQueries
from pyodbc import Connection
from datetime import datetime

# -------------------------------------------------------------------------------
#  Invoice Check Test Table
# -------------------------------------------------------------------------------


class InvoiceCheckTestTable(TestTableSpecification):
    """
    This class specifies how the test table for the invoice check test is formed.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Specify the characteristics of the test table.
        """
        super().__init__()
        self.heading = "Check that invoices exist"
        self.fixture = "castlebay.gfit.billingcenter.InvoiceCheckFixture"
        self.columns = ["TestId",
                        "Account Number",
                        "Policy Number",
                        "BillingID()",
                        "Comment"]
        self.is_unique = [False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "INVOICE-CHECK-"
        #
        # Set up query of PolicyCenter
        #
        self.pc_queries = PolicyCenterQueries(cnx)
        self.selection_end = datetime.now()
        self.number_of_rows = 10
        return

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
            model = self.convert_to_model(policy_period)
            if model.period_display_status(self.selection_end) == PolicyStatus.InForce:
                row = self.create_row(self.test_id_prefix, count, model)
                self.add_row(row)
                count += 1
        return

    @staticmethod
    def convert_to_model(policy_period) -> PolicyPeriod:
        """
        Convert the row from the policy period query to an instance of the policy period model.

        Arguments:
            policy_period - a row from the policy period query
        """
        model = PolicyPeriod()
        model.policy_number = policy_period.PolicyNumber
        model.period_start = policy_period.PeriodStart
        model.period_end = policy_period.PeriodEnd
        model.cancellation_date = policy_period.CancellationDate
        model.taxes = policy_period.Taxes
        model.premium = policy_period.Premium
        model.status = policy_period.Status
        model.billing_id = policy_period.BillingID
        model.account.account_number = policy_period.AccountNumber
        model.payment_plan = policy_period.PaymentPlan
        return model

    @staticmethod
    def create_row(prefix: str, count: int, model: PolicyPeriod) -> list[str]:
        """
        Create a row for the test table.

        Arguments:
            account - a row from a query of the account table in PolicyCenter
        """
        row = [
            prefix + str(count),
            model.account.account_number,
            model.policy_number,
            model.billing_id,
            "Check policy " + model.policy_number
        ]
        return row

# -------------------------------------------------------------------------------
#  Invoice Check Test
# -------------------------------------------------------------------------------


class InvoiceCheckTest(TestCaseSpecification):
    """
    This class specifies how the test case for the Invoice Check test case.
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
        self.suite_name = "InvoiceCheck"
        self.suite_id = "INVOICE_CHECK"
        self.description = "This test case checks that BillingCenter has the specified policy period and invoice."
        self.version = "2021-09-14"
        self.author = "W. Shaffer"
        #
        # Specify the tables in the test case
        #
        table = InvoiceCheckTestTable(cnx)
        table.generate_rows()
        self.add_test_table(table)
        return
