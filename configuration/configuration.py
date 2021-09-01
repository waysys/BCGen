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
This module contains class for configuration BC Gen programs.
"""

import base.configuration

# -------------------------------------------------------------------------------
#  Configuration
# -------------------------------------------------------------------------------

class Configuration(base.configuration.Configuration):
    """
    This class is the parent class of the other configuration classes for this
    project.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize the instance of this class.
        """
        return

    def initialize_test_class(self):
        """
        Initialize the test class that does not use InfoCenter.

        Argument:
            cls - the test class
        """
        #
        # Retrieve environmental variables for this test
        #
        print("____________________________________________________")
        print("____________________________________________________")
        return

