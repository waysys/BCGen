# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "30-Sep-2021"

"""
This module contains classes to run the BillingCenter tests suites in GFIT
"""

from configuration.gfit2020 import GFIT2020Project
from configuration.gfitwebservice import GfitWebServiceRunner

# -------------------------------------------------------------------------------
#  BillingCenter Invoice Check
# -------------------------------------------------------------------------------


class BillingCenterInvoiceCheck(GfitWebServiceRunner):
    """
    This class executes the BillingCenter Invoice Check.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, env_name: str):
        """
        Configure this instance of the class.

        Arguments:
            env_name - the name of the environment where the test is run.
        """
        super().__init__(
            GFIT2020Project(),
            env_name,
            "BC",
            "BillingCenterProject",
            "InvoiceCheck"
        )
        return

# -------------------------------------------------------------------------------
#  BillingCenter Invoice Check
# -------------------------------------------------------------------------------


class BillingCenterCommonCreate(GfitWebServiceRunner):
    """
    This class executes the PolicyCenter Homeowners Project submissions.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, env_name: str):
        """
        Configure this instance of the class.

        Arguments:
            env_name - the name of the environment where the test is run.
        """
        super().__init__(
            GFIT2020Project(),
            env_name,
            "BC",
            "BillingCenterCommonProject",
            "CommonCreate"
        )
        return

# -------------------------------------------------------------------------------
#  BillingCenter Invoice Check
# -------------------------------------------------------------------------------


class BillingCenterCollateralRequirementCreate(GfitWebServiceRunner):
    """
    This class executes the collateral requirement create test.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, env_name: str):
        """
        Configure this instance of the class.

        Arguments:
            env_name - the name of the environment where the test is run.
        """
        super().__init__(
            GFIT2020Project(),
            env_name,
            "BC",
            "BillingCenterProject",
            "CollateralRequirementCreate"
        )
        return
