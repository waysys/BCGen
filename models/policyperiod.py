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
This module models the policy period in PolicyCenter.
"""

from datetime import datetime
from enum import Enum
from decimal import Decimal


# -------------------------------------------------------------------------------
#  Policy Status
# -------------------------------------------------------------------------------


class PolicyStatus(Enum):
    """
    The policy period status.
    """
    Unbound = "Unbound"
    InForce = "In Force"
    Cancelled = "Cancelled"
    Expired = "Expired"
    Scheduled = "Scheduled"

# -------------------------------------------------------------------------------
#  Account
# -------------------------------------------------------------------------------


class Account():
    """
    This class models the account in PolicyCenter and BillingCenter.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initial this instance of the class.
        """
        self.account_number = ""
        return

# -------------------------------------------------------------------------------
#  Policy Period
# -------------------------------------------------------------------------------


class PolicyPeriod:
    """
    This class models aspects of the policy period in PolicyCenter.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize the instance of this class.
        """
        self.policy_number: str = ""
        self.period_start: datetime = datetime.now()
        self.period_end: datetime = datetime.now()
        self.cancellation_date = None
        self.status: str = "Bound"
        self.taxes: Decimal = Decimal(0)
        self.premium: Decimal = Decimal(0)
        self.billing_id: str = ""
        self.account: Account = Account()
        self.payment_plan: str = ""
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def total_invoiced_amount(self) -> Decimal:
        """
        The total amount to invoice the policy holder.
        """
        return self.premium + self.taxes

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def period_display_status(self, reporting_date: datetime) -> PolicyStatus:
        """
        Return the period display status which adjusts the status based on the current date
        and the cancellation, effective, and expiration dates of the policy period.
        """
        assert self.status is not None, "Policy period status must not be None"
        result = PolicyStatus.Unbound
        if self.status == "Bound":
            if self.cancellation_date is not None:
                result = PolicyStatus.Cancelled
            elif self.period_start > reporting_date:
                result = PolicyStatus.Scheduled
            elif self.period_end <= reporting_date:
                result = PolicyStatus.Expired
            else:
                result = PolicyStatus.InForce
        return result
