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
This module tests the GFIT2020 plan.
"""

import unittest

import xmlrunner
from configuration.gfit2020 import GFIT2020Project, ENVIRONMENT_NAME, \
    BC_APPLICATION_NAME, CC_APPLICATION_NAME, PC_APPLICATION_NAME

# -------------------------------------------------------------------------------
#  Test Web Service
# -------------------------------------------------------------------------------


class TestGFIT2020Plan(unittest.TestCase):
    """
    This class tests the GFIT2020 plan.
    """

    # -------------------------------------------------------------------------------
    #  Support Functions
    # -------------------------------------------------------------------------------

    def setUp(self):
        """
        Initialize the connection for each test.
        """
        self.project = GFIT2020Project()
        self.env_name = ENVIRONMENT_NAME
        self.test_group_name = "BillingCenterProject"
        self.ho_product_spec = "HomeownersSubmission"
        return

    def tearDown(self):
        """
        Close the connections after each test
        """
        return

    # -------------------------------------------------------------------------------
    #  Tests
    # -------------------------------------------------------------------------------

    def test_project(self):
        """
        This test checks the project.
        """
        self.assertEqual("GFIT2020", self.project.project_name)
        self.assertTrue(self.project.project_description is not None, "Project description was not set")
        self.assertTrue(self.project.is_base_dir_valid,
                        "Base directory is not valid: " + self.project.test_suite_base_dir)
        return

    def test_environment(self):
        """
        This test checks that the environment is set up.
        """
        self.assertTrue(self.project.has_environment(self.env_name), "Environment not found: " + self.env_name)
        environment = self.project.fetch_environment(self.env_name)
        self.assertTrue(environment is not None, "Environment not fetched: " + self.env_name)
        self.assertTrue(environment.is_output_base_dir_valid,
                        "Output base directory does not exist: " + environment.test_output_base_dir)
        #
        # Check application
        #
        self.assertTrue(environment.has_application(BC_APPLICATION_NAME),
                        "Application not found: " + BC_APPLICATION_NAME)
        application = environment.fetch_application(BC_APPLICATION_NAME)
        self.assertTrue(application is not None,
                        "Application not fetched: " + BC_APPLICATION_NAME)
        #
        # Check output directory
        #
        self.assertTrue(environment.is_output_base_dir_valid,
                        "Output base directory does not exist: " + environment.test_output_base_dir)
        self.assertTrue(environment.is_output_dir_valid(self.test_group_name),
                        "Output directory does not exist")
        return

    def test_group_creation(self):
        """
        This test checks that test groups can be created.
        """
        self.assertTrue(self.project.has_test_group(self.test_group_name),
                        "Project does not have test group: " + self.test_group_name)
        test_group = self.project.fetch_test_group(self.test_group_name)
        self.assertTrue(test_group is not None, "Test group not fetched")
        self.assertTrue(test_group.is_test_group_base_dir_valid, "Test group base directory does not exist")
        return

    def test_database_definition(self):
        """
        This test checks the database definition.
        """
        self.assertTrue(self.project.has_environment(self.env_name), "Environment not found: " + self.env_name)
        environment = self.project.fetch_environment(self.env_name)
        self.assertTrue(environment is not None, "Environment not fetched: " + self.env_name)
        self.assertTrue(environment.is_output_base_dir_valid,
                        "Output base directory does not exist: " + environment.test_output_base_dir)
        #
        # Check BillingCenter application
        #
        self.assertTrue(environment.has_application(BC_APPLICATION_NAME),
                        "Application not found: " + BC_APPLICATION_NAME)
        application = environment.fetch_application(BC_APPLICATION_NAME)
        self.assertTrue(application is not None,
                        "Application not fetched: " + BC_APPLICATION_NAME)
        self.assertTrue(application.is_database_valid, "Database check failed")
        #
        # Check ClaimCenter application
        #
        self.assertTrue(environment.has_application(CC_APPLICATION_NAME),
                        "Application not found: " + CC_APPLICATION_NAME)
        application = environment.fetch_application(BC_APPLICATION_NAME)
        self.assertTrue(application is not None,
                        "Application not fetched: " + CC_APPLICATION_NAME)
        self.assertTrue(application.is_database_valid, "Database check failed")
        return

    def test_product_spec_definition(self):
        """
        Test for the product specification.
        """
        self.assertTrue(self.project.has_application_type(BC_APPLICATION_NAME),
                        "Application type not found: " + BC_APPLICATION_NAME)
        self.assertTrue(self.project.has_application_type(PC_APPLICATION_NAME),
                        "Application type not found: " + PC_APPLICATION_NAME)
        self.assertTrue(self.project.has_application_type(CC_APPLICATION_NAME),
                        "Application type not found: " + CC_APPLICATION_NAME)
        applicaton_type = self.project.fetch_application_type(PC_APPLICATION_NAME)
        self.assertTrue(applicaton_type.has_product_spec(self.ho_product_spec),
                        "Product spec not found: " + self.ho_product_spec)
        #
        # Test specification file
        #
        product_spec = applicaton_type.fetch_product_spec(self.ho_product_spec)
        self.assertTrue(product_spec.is_product_spec_file_valid,
                        "Invalid product spec file: " + product_spec.product_spec_file)
        return

# -------------------------------------------------------------------------------
#  Main Program
# -------------------------------------------------------------------------------


if __name__ == '__main__':
    report_file = '/GFITWorkspaces/COMMON01/plan_test.xml'
    with open(report_file, 'w') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
