# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "10-Oct-2021"

"""
This module specifies the collateral requirement test case.
"""

from datetime import datetime

from pyodbc import Connection

from base.testrandom import Random, DEFAULT_SEED
from base.uniqueid import gen_unique_id
from base.dates import convert_to_iso_string
from models.spec import TestTableSpecification, TestCaseSpecification
from queries.policycenterqueries import PolicyCenterQueries

# -------------------------------------------------------------------------------
#  Write-Off Make Test Table
# -------------------------------------------------------------------------------


class CollateralRequirementTestTable(TestTableSpecification):
    """
    This class specifies how the collateral requirement test table is formed.
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
        self.heading = "Create collateral requirement"
        self.fixture = "castlebay.gfit.billingcenter.CollateralRequirementCreateFixture"
        self.columns = ["TestId",
                        "Account Number",
                        "Requirement Name",
                        "Requirement Amount",
                        "Requirement Type",
                        "Effective Date",
                        "Expiration Date",
                        "Valid()",
                        "Comment"]
        self.is_unique = [False, False, True, False, False, False, False, False, False]
        self.test_id_start = 10
        self.test_id_prefix = "COLL-REQ-"
        self.ref_prefix = gen_unique_id()
        self.collateral_range = (1000, 5000)
        #
        # Set up query of PolicyCenter
        #
        self.pc_queries = PolicyCenterQueries(cnx)
        self.selection_end = datetime.now()
        self.number_of_rows = 1
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def collateral_amount(self) -> str:
        """
        Return a random collateral amount in dollars.
        """
        return self.random.get_random(self.collateral_range)

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
            policy_period.AccountNumber,
            "Cash Requirement - ",
            self.collateral_amount,
            "cash",
            self.comp_effective_date(policy_period),
            self.comp_expiration_date(policy_period),
            "true",
            "Create collateral requirement"
        ]
        return row

    @staticmethod
    def comp_effective_date(policy_period) -> str:
        """
        Compute a valid effective date for the collateral requirement based on the effective date of the
        policy period.

        Arguments:
            policy_period - a row from the PolicyPeriod query
        """
        period_start = policy_period.PeriodStart
        effective_date = max(datetime.now(), period_start)
        result = convert_to_iso_string(effective_date)
        return result

    @staticmethod
    def comp_expiration_date(policy_period) -> str:
        """
        Compute a valid expiration date for the collateral requirement base on the period end of the policy
        period.  Return a string in the ISO format YYYY-MM-DD.

        Arguments:
            policy_period - a row from the PolicyPeriod query
        """
        period_end = policy_period.PeriodEnd
        expiration_date = max(datetime.now(), period_end)
        result = convert_to_iso_string(expiration_date)
        return result

# -------------------------------------------------------------------------------
#  Payment Make Test
# -------------------------------------------------------------------------------


class CollateralRequirementTest(TestCaseSpecification):
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
        self.suite_name = "CollateralRequirementCreate"
        self.suite_id = "COLL-REQ"
        self.description = \
            """
            This test case creates new collateral requirements for accounts with new policies.
            """
        self.version = "2021-10-10"
        self.author = "W. Shaffer"
        self.repeatable = "Yes"
        #
        # Specify the tables in the test case
        #
        table = CollateralRequirementTestTable(cnx)
        table.generate_rows()
        self.add_test_table(table)
        return
