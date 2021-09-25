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

from base.configuration import Configuration
from configuration.gfit2020 import Project


# -------------------------------------------------------------------------------
#  Connector Test Configuration
# -------------------------------------------------------------------------------


class ConnectorTestConfiguration(Configuration):
    """
    This class contains the configuration for the connector test module.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize the instance of this class.
        """
        project = Project()
        super().__init__(project)
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------



    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def initialize_test_class(self):
        """
        Initialize the test class that does not use InfoCenter.
        """
        #
        # Retrieve environmental variables for this test
        #
        print("____________________________________________________")
        print("ODBC connector: " + self.data_source)
        print("Database: " + self.database)
        print("____________________________________________________")
        return
