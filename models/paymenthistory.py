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
This module contains the PaymentHistory class that supports maintaining a
history of payments.
"""

from decimal import Decimal

# -------------------------------------------------------------------------------
#  Payment History
# -------------------------------------------------------------------------------


class PaymentHistory:

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, ref_number: str, account_number: str, applied: bool, reversed: bool):
        """
        Initialize an instance of this class.

        Arguments:
            ref_number - reference number of the payment
            applied - true if the payment is being applied
            reversed - true if the payment is being reversed

        """
        self.ref_number = ref_number
        self.account_number = account_number
        self.policy_number = None
        self.applied = applied
        self.reversed = reversed
        self.disbursed = False
        return