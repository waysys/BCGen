# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#

__author__ = 'Bill Shaffer'
__version__ = "25-Sep-2021"

"""
This module contains a class that is the parent of classes that 
handle the environment configurations (source
databases, destination databases, and report locations) for various 
types of tests.
"""

import os
import sys
from datetime import datetime

from base.connector import Database
from base.dates import process_env_date
from base.plan import Project, Environment


# -------------------------------------------------------------------------------
#  Configuration
# -------------------------------------------------------------------------------


class Configuration:
    """
    This class is the parent of the classes that define the configurations for tests.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, project: Project):
        """
        Initialize this instance of the class.

        Arguments:
            project - the project object for this configuration
        """
        assert project is not None, "Project must not be None"
        self.project = project
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def reporting_date(self) -> datetime:
        """
        Return the reporting date.
        """
        env_date = os.getenv("ENV_DATE", "current")
        date = process_env_date(env_date)
        return date

    @property
    def starting_date(self) -> datetime:
        """
        Return the starting date for a range of data.
        """
        env_date = os.getenv("ENV_START_DATE", "current")
        date = process_env_date(env_date)
        return date

    @property
    def today(self) -> datetime:
        """
        Return the current date and time.
        """
        today = datetime.now()
        return today

    # ---------------------------------------------------------------------------
    #  Functions for obtaining database information
    # ---------------------------------------------------------------------------

    def get_database_info(self, env_variable_name, application_name) -> Database:
        """
        Retrieve the data source and database based on the environment variable name.
        Retrieve the environment abbreviation from the system and then retrieve the database information
        from the list of environments.
        """
        assert env_variable_name is not None, "Environment variable name must not be None"
        assert application_name is not None, "Application number must not be None"
        environment = self.fetch_environment(env_variable_name)
        assert environment.has_application(application_name), \
            "Environment does not have application: " + application_name
        application = environment.fetch_application(application_name)
        database = application.database
        assert database is not None, "Application does not have a database"
        return database

    def initialize_test_class(self):
        """
        Initialize the test class.  This function should be implemented in the subclass.
        """
        raise NotImplementedError

    # -------------------------------------------------------------------------------
    # Functions for obtaining the environment object
    # -------------------------------------------------------------------------------

    def has_environment(self, env_name: str) -> bool:
        """
        Return true if the environment is supported in this project.

        Argument:
            env_name - the name of the environment.
        """
        return self.project.has_environment(env_name)

    def get_environment(self, env_name) -> Environment:
        """
        Return the environment object with the specified name.

        Arguments:
            environ - the name of the environment
        """
        result = self.project.fetch_environment(env_name)
        return result

    def fetch_environment(self, environ_variable) -> Environment:
        """
        Fetch the environment name from the environment variables in the operating system.
        Use the name to fetch the environment object.

        Arguments:
            environ_variable - the environmental variable that has the code
            default - the default code if the environmental variable does not exist
        """
        assert environ_variable is not None, "Environmental variable must not be None"
        env_name = os.getenv(environ_variable)
        assert env_name is not None, "Environment variable is not set: " + environ_variable
        if not self.has_environment(env_name):
            print("Unknown environment: " + environ_variable)
            sys.exit(1)
        environment = self.get_environment(env_name)
        return environment

    # -------------------------------------------------------------------------------
    # Functions for obtaining the test report path
    # -------------------------------------------------------------------------------

    def test_report(self, env_name, test_group_name, test_suite_name) -> str:
        """
        Return the full path of the test report including name but not extension.
        """
        assert test_group_name is not None, "Test group must not be None"
        assert test_suite_name is not None, "Test suite must not be None"
        assert self.project.has_test_group(test_group_name), "Project does not have test group: " + test_group_name
        test_group = self.project.fetch_test_group(test_group_name)
        assert test_group.has_test_suite(test_suite_name), \
            "Test group " + test_group_name + " does not have test suite: " + test_suite_name
        test_suite = test_group.fetch_test_suite(test_suite_name)
        path = test_suite.test_suite_output(env_name)
        return path
