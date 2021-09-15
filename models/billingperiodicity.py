# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "13-Sep-2021"

"""
This module models the billing periodicity typelist in PolicyCenter.
"""

from enum import Enum


# -------------------------------------------------------------------------------
#  Billing Periodicity
# -------------------------------------------------------------------------------


class BillingPeriodicity(Enum):
    """
    This class defines the periodicity used in invoice.  The value of the enum is
    the number of invoices per year.
    """

    everyfourmonths = 3
    everyothermonth = 6
    everyotherweek = 26
    everyotheryear = 0
    everysixmonths = 2
    everyweek = 52
    everyyear = 1
    monthly = 12
    quarterly = 4
    twicepermonth = 24

    @property
    def number_invoices(self):
        """
        Return the number of invoices sent for each periodicity.
        """
        return self.value

    @property
    def number_installments(self):
        """
        Return the number of installments for each periodicity.
        """
        return self.value - 1

    @classmethod
    def has_periodicity(cls, name):
        """
        Return true if name is a valid name of a periodicity.

        Arguments:
            name - the name of a periodicity to be tested
        """
        result = True
        try:
            BillingPeriodicity[name]
        except KeyError:
            result = False
        return result
