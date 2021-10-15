# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "26-Sep-2021"

"""
This module executes GFIT tests using the Python GFIT client.
"""

import sys

from configuration.gfit2020 import GFIT2020Project
from configuration.gfitwebservice import GfitWebServiceRunner


# -------------------------------------------------------------------------------
#  PolicyCenter Homeowners Submission
# -------------------------------------------------------------------------------


class PolicyCenterHomeownersSubmission(GfitWebServiceRunner):
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
            "PC",
            "PolicyCenterHomeownersProject",
            "HomeownersSubmission"
        )
        application_type = self.project.fetch_application_type("PC")
        product_spec = application_type.fetch_product_spec("HomeownersSubmission")
        assert product_spec.is_product_spec_file_valid, \
            "Product spec file not found: " + product_spec.product_spec_file
        self.product_spec_file = product_spec.product_spec_file
        test_group = self.project.fetch_test_group("PolicyCenterHomeownersProject")
        self.test_group_directory = test_group.test_group_base_dir
        return


# -------------------------------------------------------------------------------
#  PolicyCenter Homeowners Submission
# -------------------------------------------------------------------------------


class PolicyCenterHomeownersAccountCreate(GfitWebServiceRunner):
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
            "PC",
            "PolicyCenterAccountProject",
            "AccountCreate"
        )
        return


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    """
    Run the test generation program
    """
    policycenter_client = PolicyCenterHomeownersSubmission("COMMON01")
    reslt = policycenter_client.run_test()
    exit_code = 0 if reslt else 1
    sys.exit(exit_code)
