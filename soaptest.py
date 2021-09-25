# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "23-Sep-2021"

"""
This module tests the operation of Zeep as a SOAP web service
"""

import unittest

import xmlrunner

from base.gfitclient import GfitClient


# -------------------------------------------------------------------------------
#  Test Web Service
# -------------------------------------------------------------------------------


class TestWebService(unittest.TestCase):
    """
    This class contains methods to test using Zeep to invoke the GFIT Web Service.
    """

    url = "http://localhost:8580/bc/ws/castlebay/gfit/GfitAPI?wsdl"

    # -------------------------------------------------------------------------------
    #  Support Functions
    # -------------------------------------------------------------------------------

    def setUp(self):
        """
        Initialize the connection for each test.
        """
        self.testsuite = "/git/GfitSupport/TESTSUITES/BC/BillingCenterProject/AccountPaymentMake"
        self.reportname = "/GFITWorkspaces/COMMON01/BillingCenterProject/AccountPaymentMake"
        return

    def tearDown(self):
        """
        Close the connections after each test
        """
        return

    # -------------------------------------------------------------------------------
    #  Tests
    # -------------------------------------------------------------------------------

    def test_gfit_client(self):
        """
        This test checks that the GFIT client works correctly.
        """
        gfit_client = GfitClient(self.url)
        result = gfit_client.run(self.testsuite, self.reportname)
        self.assertEqual(True, result, "GFIT execution failed")
        return

    def test_wsdl_url_validation(self):
        """
        This test checks the WSDL URL validation.
        """
        result = GfitClient.is_valid_wsdl(self.url)
        self.assertTrue(result, "validation failed to return True")
        result = GfitClient.is_valid_wsdl("http://bozo.com/ws?wsdl")
        self.assertTrue(not result, "Validation failed to return Fals")
        return


# -------------------------------------------------------------------------------
#  Main Program
# -------------------------------------------------------------------------------


if __name__ == '__main__':
    report_file = '/GFITWorkspaces/COMMON01/soap_test.xml'
    with open(report_file, 'w') as output:
        unittest.main(
            testRunner=xmlrunner.XMLTestRunner(output=output),
            failfast=False, buffer=False, catchbreak=False)
