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
This modules specifies the payment plan change test case.
"""

from datetime import datetime

from pyodbc import Connection

from base.testrandom import Random, DEFAULT_SEED
from models.spec import TestTableSpecification, TestCaseSpecification
from queries.policycenterqueries import PolicyCenterQueries


# -------------------------------------------------------------------------------
#  Payment Plan Change Test Table
# -------------------------------------------------------------------------------


class PaymentPlanChangeTestTable(TestTableSpecification):
    """
    This class specifies how the payment plan change test table is formed.
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
        self.heading = "Change payment plans"
        self.fixture = "castlebay.gfit.billingcenter.PaymentPlanChangeFixture"
        self.columns = ["TestId",
                        "Account Number",
                        "Policy Number",
                        "PaymentPlanID",
                        "Valid()",
                        "Comment"]
        self.is_unique = [False, False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "PAYMENT-PLAN-CHANGE-"
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
        new_id = self.select_payment_plan_id(policy_period)
        row = [
            prefix + str(count),
            policy_period.AccountNumber,
            policy_period.PolicyNumber,
            new_id,
            "true",
            "Change payment plan from " + policy_period.PaymentPlan
        ]
        return row

    def select_payment_plan_id(self, policy_period):
        """
        Return a payment plan id other than the current payment plan.

        Arguments:
            policy_period - the result of the policy period query
        """
        billing_id = policy_period.BillingID
        available_plans = self.pc_queries.query_payment_plan(billing_id)
        ids = self.form_list_of_billing_ids(available_plans)
        new_id = self.random.select_from_list(ids)
        return new_id

    @staticmethod
    def form_list_of_billing_ids(available_plans: list) -> list[str]:
        """
        Return a list of the billing ids from the records retrieed from PolicyCenter.

        Arguments:
            available_plans - the results from the query of BillingCenter
        """
        ids = []
        for plan in available_plans:
            ids.append(plan.BillingID)
        return ids

# -------------------------------------------------------------------------------
#  Payment Make Test
# -------------------------------------------------------------------------------


class PaymentPlanChangeTest(TestCaseSpecification):
    """
    This class specifies how the test case for the Payment Plan Change test case.
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
        self.suite_name = "PaymentPlanChange"
        self.suite_id = "PAYMENT-PLAN_CHANGE"
        self.description = \
            """
            This test case creates tests to change the payment plans on policies in BillingCenter.
            The test case is repeatable, but once the payment plan is changed to the one in the test,
            repeating the test will result in a warning and no change.
            """
        self.version = "2021-09-20"
        self.author = "W. Shaffer"
        self.repeatable = "Yes"
        #
        # Specify the tables in the test case
        #
        table = PaymentPlanChangeTestTable(cnx)
        table.generate_rows()
        self.add_test_table(table)
        return
