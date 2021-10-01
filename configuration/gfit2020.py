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

from base.connector import Database, Access
from base.plan import Project, Environment

PROJECT_NAME = "GFIT2020"
ENVIRONMENT_NAME = "COMMON01"
BC_APPLICATION_NAME = "BC"
PC_APPLICATION_NAME = "PC"
CC_APPLICATION_NAME = "CC"


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
        # Application Types
        #
        self.define_application_types()
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
        assert self.is_base_dir_valid, "Test suite base directory is invalid: " + self.test_suite_base_dir
        self.product_spec_base_dir = "C:/git/GfitSupport/PRODUCT_SPEC"
        assert self.is_product_spec_dir_valid, "Product spec base directory is invalid: " + self.product_spec_base_dir
        return

    def define_application_types(self):
        """
        Define the application types.
        """
        application_type = self.create_application_type(BC_APPLICATION_NAME)
        application_type.application_type_description = "BillingCenter"
        application_type = self.create_application_type(CC_APPLICATION_NAME)
        application_type.application_type_description = "ClaimCenter"
        application_type = self.create_application_type(PC_APPLICATION_NAME)
        application_type.application_type_description = "PolicyCenter"
        pc_product_spec = application_type.create_product_spec("HomeownersSubmission")
        pc_product_spec.product_spec_description = "Specification for HO policies"
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
        #
        # PolicyCenter application
        #
        application = environment.create_application(PC_APPLICATION_NAME)
        application.application_description = """
        PolicyCenter
        """
        application.database = self.define_pc_database()
        application.web_service = "http://localhost:8180/pc/ws/castlebay/gfit/GfitAPI?wsdl"
        #
        # ClaimCenter application
        #
        application = environment.create_application(CC_APPLICATION_NAME)
        application.application_description = "ClaimCenter"
        application.database = self.define_cc_database()
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
        database.server = "PORTAL15\\SQLEXPRESS"
        return database

    @staticmethod
    def define_pc_database() -> Database:
        """
        Define the database for BillingCenter.
        """
        database = Database()
        database.name = "PolicyCenter"
        database.access = Access.Windows
        database.data_source = "COMMON01"
        database.db_name = "GWPC"
        database.server = "PORTAL15\\SQLEXPRESS"
        return database

    @staticmethod
    def define_cc_database() -> Database:
        """
        Define the database for BillingCenter.
        """
        database = Database()
        database.name = "ClaimCenter"
        database.access = Access.Windows
        database.data_source = "COMMON01"
        database.db_name = "GWCC"
        database.server = "PORTAL15\\SQLEXPRESS"
        return database

    def define_test_group(self):
        """
        Define the test groups associated with this project.
        """
        #
        # BillingCenter Project
        #
        self.define_bc_test_group()
        #
        # PolicyCenter Project
        #
        self.define_pc_test_group()
        self.define_pc_homeowners_test_group()
        self.define_pc_account_create_group()
        return

    def define_bc_test_group(self):
        """
        Define the BillingCenterProject test group.
        """
        test_group = self.create_test_group("BillingCenterProject")
        test_group.test_group_description = """
         This test group contains test suites that check GFIT fixtures for BillingCenter.
         """
        application_type = self.fetch_application_type(BC_APPLICATION_NAME)
        test_group.application_type = application_type
        test_group.create_test_suite("InvoiceCheck")
        test_group.create_test_suite("MakePayments")
        test_group.create_test_suite("SuspensePaymentMake")
        return

    def define_pc_test_group(self):
        """
        Define the PolicyCenterProject test group.
        """
        test_group = self.create_test_group("PolicyCenterProject")
        test_group.test_group_description = """
         This test group contains test suites that test PolicyCenter.
         """
        application_type = self.fetch_application_type(PC_APPLICATION_NAME)
        test_group.application_type = application_type
        test_group.create_test_suite("connectortest")
        return

    def define_pc_homeowners_test_group(self):
        """
        Define the PolicyCenterHomeowners test group.
        """
        test_group = self.create_test_group("PolicyCenterHomeownersProject")
        test_group.test_group_description = """
         This test group contains test suites that create and manipulate policies in PolicyCenter.
         """
        application_type = self.fetch_application_type(PC_APPLICATION_NAME)
        test_group.application_type = application_type
        test_group.create_test_suite("HomeownersSubmission")
        return

    def define_pc_account_create_group(self):
        """
        Defined the PolicyCenterAccountProject and AccountCreate test suite.
        """
        test_group = self.create_test_group("PolicyCenterAccountProject")
        test_group.test_group_description = """
        This test group contains the test suite to create some accounts for use in other tests.
        This test group is an initialize group and can be run only once after dropping the database.
        """
        application_type = self.fetch_application_type(PC_APPLICATION_NAME)
        test_group.application_type = application_type
        test_group.create_test_suite("AccountCreate")
        return
