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

    @property
    def data_source(self) -> str:
        """
        Return the name of the ODBC data source.
        """
        return self.db_source[0]

    @property
    def database(self) -> str:
        """
        Return the name of the database.
        """
        return self.db_source[1]

    def initialize_test_class(self):
        """
        Initialize the test class that does not use InfoCenter.
        """
        #
        # Retrieve environmental variables for this test
        #
        print("____________________________________________________")
        print("____________________________________________________")
        return

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
        super().__init__()
        return

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
