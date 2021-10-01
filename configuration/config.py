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
from configuration.gfit2020 import GFIT2020Project, ENVIRONMENT_NAME, PC_APPLICATION_NAME, Access, Environment
from base.connector import Database


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
        project = GFIT2020Project()
        super().__init__(project)
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def environment(self) -> Environment:
        """
        Return the environment specified for this execution.
        """
        env = self.fetch_environment("ENV_ENV")
        return env

    @property
    def env_name(self) -> str:
        """
        Return the name of the environment.
        """
        return self.environment.env_name

    @property
    def data_source(self) -> Database:
        """
        Return the database definition for this test suite.
        """
        application = self.environment.fetch_application(PC_APPLICATION_NAME)
        assert application.database is not None, \
            "Application " + PC_APPLICATION_NAME + " does not have database definition"
        return application.database

    @property
    def report_file(self):
        """
        Return the full path of the reporting file.
        """
        test_group = self.project.fetch_test_group("PolicyCenterProject")
        test_suite = test_group.fetch_test_suite("connectortest")
        report_file = test_suite.test_suite_output(self.env_name)
        report_file += ".xml"
        return report_file

    @property
    def test_suite_directory(self) -> str:
        """
        Return the path of the directory that holds the test suites.
        """
        assert self.project.is_base_dir_valid, \
            "Test group base directory is invalid: " + self.project.test_suite_base_dir
        diry = self.project.test_suite_base_dir
        return diry

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
        print("Environment: " + self.env_name)
        if self.data_source == Access.Windows:
            print("ODBC connector: " + self.data_source.data_source)
        print("Database server: " + self.data_source.server)
        print("Database: " + self.data_source.db_name)
        print("Report file: " + self.report_file)
        print("____________________________________________________")
        return

# -------------------------------------------------------------------------------
#  PolicyCenterHomeownersProject Configuration
# -------------------------------------------------------------------------------


class PolicyCenterHomeownersProjectConfiguration(ConnectorTestConfiguration):
    """
    This class provides the parameters for executing the GFIT tests suites in the
    PolicyCenter Homeowners Project.
    """

    def __init__(self):
        """
        Initialize an instance of this class.
        """
        super().__init__()
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def output_file(self) -> str:
        """
        Provide the full path including the file name (without extension) for the GFIT output.
        """
        test_group = self.project.fetch_test_group("PolicyCenterHomeownersProject")
        test_suite = test_group.fetch_test_suite("HomeownersSubmission")
        report_file = test_suite.test_suite_output(ENVIRONMENT_NAME)
        return report_file

    @property
    def wsdl(self) -> str:
        """
        Provide the URL for the WSDL for the GFIT web service on the appropriate application.
        """
        application = self.environment.fetch_application(PC_APPLICATION_NAME)
        return application.web_service

    @property
    def username(self):
        """
        The user name for the GFIT web service.
        """
        return "su"

    @property
    def password(self):
        """
        The password for the GFIT web service
        """
        return "gw"

    @property
    def test_suite_directory(self) -> str:
        """
        Return the path of the directory that holds the test suites.
        """
        assert self.project.is_base_dir_valid, \
            "Test group base directory is invalid: " + self.project.test_suite_base_dir
        test_group = self.project.fetch_test_group("PolicyCenterHomeownersProject")
        test_suite = test_group.fetch_test_suite("HomeownersSubmission")
        diry = test_suite.test_suite_dir
        assert diry, "Test suite directory does not exist: " + diry
        return diry