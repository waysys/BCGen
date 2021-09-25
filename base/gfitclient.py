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
This module provides a client for calling the GFIT web service in Guidewire
InsuranceSuite applications.
"""

from zeep import Client, xsd


# -------------------------------------------------------------------------------
#  GFIT Client
# -------------------------------------------------------------------------------


class GfitClient:
    """
    This class provides a client for calling the GfitAPI web service.  This class
    uses the Python module Zeep.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, wsdl_url: str):
        """
        Initialize an instance of this class.

        Arguments:
            wsdl_url - the universal resource locator for the WSDL associated with the GFIT web service.
        """
        assert wsdl_url is not None, "the WSDL URL must not be None"
        assert len(wsdl_url) > 0, "the WSDL URL must not be an empty string"
        self.client = Client(wsdl_url)
        self.header = self.create_header()
        self.username = "su"
        self.password = "gw"
        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    @staticmethod
    def create_header() -> xsd.Element:
        """
        Create the header for the SOAP call.
        """
        header = xsd.Element('{http://guidewire.com/ws/soapheaders}authentication', xsd.ComplexType([
            xsd.Element('{http://guidewire.com/ws/soapheaders}username', xsd.String()),
            xsd.Element('{http://guidewire.com/ws/soapheaders}password', xsd.String())
        ])
                             )
        return header

    def run(self, test_suite: str, report_name: str) -> bool:
        """
        Invoke the GFIT API web service with the specified test suite and report output.
        Return True if the execution was successful.  Otherwise, return False

        Arguments:
            test_suite - the full path to the test suite directory that holds the test cases
            report_name - the directory path and name of the report files
        """
        assert test_suite is not None, "Test suite path must not be None"
        assert len(test_suite) > 0, "Test suite path must not be an empty string"
        assert report_name is not None, "Report name must not be None"
        assert len(report_name) > 0, "Report name must not be an empty string"
        result = False
        header_value = self.header(username=self.username, password=self.password)
        try:
            resp = self.client.service.run(dir=test_suite, output=report_name, _soapheaders=[header_value])
        except Exception as e:
            print("Exception thrown: " + str(e))
            raise e
        if resp == "true":
            result = True
        return result

    @classmethod
    def is_valid_wsdl(cls, wsdl_url: str) -> bool:
        """
        Return True if the URL for the WSDL is valid.
        """
        assert wsdl_url is not None, "the WSDL URL must not be None"
        assert len(wsdl_url) > 0, "the WSDL URL must not be an empty string"
        try:
            Client(wsdl_url)
            result = True
        except Exception:
            result = False
        return result
