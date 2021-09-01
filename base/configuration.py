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
This module contains a class that is the parent of classes that 
handle the environment configurations (source
databases, destination databases, and report locations) for various 
types of tests.
"""

from datetime import datetime
import os

from base.environments import fetch_environment_code, has_environment
from base.dates import process_env_date
from base.testexception import TestException

# -------------------------------------------------------------------------------
#  Report Files
# -------------------------------------------------------------------------------

report_files = {

}

# -------------------------------------------------------------------------------
#  Configuration
# -------------------------------------------------------------------------------


class Configuration:
    """
    This class is the parent of the classes that vary by the nature of the test.
    """
    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize this instance of the class.
        """
        return

    @property
    def db_source(self):
        """
        Return the database information for the source.
        """
        env_name = "ENV_SOURCE"
        param = self.get_database_info(env_name)
        return param

    @property
    def db_dest(self):
        """
        Return the database information for the destination.
        """
        env_name = "ENV_DEST"
        param = self.get_database_info(env_name)
        return param

    @property
    def db_info(self):
        """
        Return the database information for InfoCenter
        """
        env_name = "ENV_INFO"
        param = self.get_database_info(env_name)
        return param

    @property
    def reporting_date(self):
        """
        Return the reporting date.
        """
        env_date = os.getenv("ENV_DATE", "current")
        date = process_env_date(env_date)
        return date

    @property
    def starting_date(self):
        """
        Return the starting date for a range of data.
        """
        env_date = os.getenv("ENV_START_DATE", "current")
        date = process_env_date(env_date)
        return date

    @property
    def report_file(self):
        """
        Return the full path to the test report.
        """
        return self.test_report()

    @property
    def today(self):
        """
        Return the current date and time.
        """
        today = datetime.now()
        return today

    @staticmethod
    def get_database_info(env_variable_name):
        """
        Retrieve the database environment information based on the environment variable name.
        Retrieve the environment abbreviation from the system and then retrieve the database information
        from the list of environments.
        """
        assert env_variable_name is not None, "Environment variable name must not be None"
        env_abbreviation = fetch_environment_code(env_variable_name, "Environment Variable Not Specified")
        if not has_environment(env_abbreviation):
            raise TestException("Unknown environment name - " + env_abbreviation)
        return env_abbreviation

    def initialize_test_class(self):
        """
        Initialize the test class.  This function should be implemented in the subclass.
        """
        return

    # -------------------------------------------------------------------------------
    # Functions for obtaining the test report path
    # -------------------------------------------------------------------------------

    @staticmethod
    def test_report():
        """
        Return the full path of the test report.
        """
        abbrev = fetch_environment_code("ENV_REPORT", "XX")
        if abbrev == 'XX':
            raise TestException("Environment variable ENV_REPORT is not set")
        if abbrev in report_files:
            result = report_files[abbrev]
        else:
            raise TestException("Environment is not listed in report files - " + abbrev)
        return result

    # -------------------------------------------------------------------------------
    # Reporting Date Functions
    # -------------------------------------------------------------------------------

    @staticmethod
    def fetch_reporting_date():
        """
        Return the reporting date from the environmental variable ENV_DATE.
        """
        env_date = os.getenv("ENV_DATE", "current")
        date = process_env_date(env_date)
        return date