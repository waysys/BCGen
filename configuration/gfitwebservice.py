# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "30-Sep-2021"

"""
This module contains the parent class for running GFIT web services.
"""

from datetime import datetime

from base.gfitclient import GfitClient
from base.plan import Project

# -------------------------------------------------------------------------------
#  GFIT Web Service Runner
# -------------------------------------------------------------------------------


class GfitWebServiceRunner:
    """
    This class is the parent of lasses that execute specific test cases.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self,
                 project: Project,
                 env_name: str,
                 app_name: str,
                 test_group_name: str,
                 test_suite_name: str):
        """
        Configure this instance of the class.
        """
        assert project is not None, "Project must not be None"
        self.project = project
        environment = project.fetch_environment(env_name)
        application = environment.fetch_application(app_name)
        self.client = GfitClient(application.web_service)
        self.client.username = "su"
        self.client.password = "gw"
        test_group = project.fetch_test_group(test_group_name)
        self.test_suite = test_group.fetch_test_suite(test_suite_name)
        self.test_suite_directory = self.test_suite.test_suite_dir
        self.output_file = self.test_suite.test_suite_output(env_name)
        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def run_test(self):
        """
        Run the GFIT test.
        """
        now = datetime.now()
        print("Starting GFIT test: " + self.test_suite.test_suite_name + " at " + str(now))
        result = self.client.run(self.test_suite_directory, self.output_file)
        now = datetime.now()
        if result:
            print("Test suite succeeded at: " + str(now))
        else:
            print("Test suite had errors at: " + str(now))
        return result
