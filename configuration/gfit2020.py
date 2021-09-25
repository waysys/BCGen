# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "24-Sep-2021"

"""
This module defines the configuration for the GFIT2020 project.
"""

from base.plan import Project, Environment
from base.connector import Database, Access

PROJECT_NAME = "GFIT2020"
ENVIRONMENT_NAME = "COMMON01"
BC_APPLICATION_NAME = "BC"

# -------------------------------------------------------------------------------
#  GFIT2020 Project
# -------------------------------------------------------------------------------


class GFIT2020Project(Project):
    """
    This class contains the configuration for the GFIT2020 project.  This project provides for
    automated testing of GFIT2020.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Configure an instance of this class.
        """
        super().__init__()
        #
        # Project Configuration
        #
        self.define_project()
        #
        # Generate environment
        #
        self.define_environment()
        #
        # Generate test groups
        #
        self.define_test_group()
        return

    def define_project(self):
        """
        Define the configuration at the project level.
        """
        self.project_name = PROJECT_NAME
        self.project_description = """
        This project generates test cases for testing the most recent version of GFIT for PolicyCenter,
        ClaimCenter, and BillingCenter.
        """
        self.test_suite_base_dir = "C:/git/GfitSupport/TESTSUITES"
        return

    def define_environment(self):
        """
        Define the environments for this test case.
        """
        environment = self.create_environment(ENVIRONMENT_NAME)
        environment.env_description = """
        This environment operates on the Google COMMON01 virtual machines.  It runs the out-of-the-box versions
        of PolicyCenter, ClaimCenter, and BillingCenter Version 10.
        """
        environment.test_output_base_dir = "/GFITWorkspaces"
        #
        # Define the applications in this environment
        #
        self.define_applications(environment)
        return

    def define_applications(self, environment: Environment):
        """
        Define the applications for this environment.

        Arguments:
            environment - the environment to which this application belongs
        """
        #
        # BillingCenter application
        #
        application = environment.create_application(BC_APPLICATION_NAME)
        application.application_description = """
        BillingCenter
        """
        application.database = self.define_bc_database()
        application.web_service = "http://localhost:8580/bc/ws/castlebay/gfit/GfitAPI?wsdl"
        return

    @staticmethod
    def define_bc_database() -> Database:
        """
        Define the database for BillingCenter.
        """
        database = Database()
        database.name = "BillingCenter"
        database.access = Access.Windows
        database.data_source = "COMMON01"
        database.db_name = "GWBC"
        return database

    def define_test_group(self):
        """
        Define the test groups associated with this project.
        """
        test_group = self.create_test_group("BillingCenterProject")
        test_group.test_group_description = """
        This test group contains test suites that check GFIT fixtures for BillingCenter.
        """
        application = self.fetch_environment(ENVIRONMENT_NAME).fetch_application(BC_APPLICATION_NAME)
        test_group.application = application
        return
