# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "06-Sep-2021"

"""
This module contains the main program for generating GFIT test cases.  The test
case generation framework uses a test case specification to generate HTML
test case files for the GFIT tool for testing Guidewire InsuranceSuite applications.
"""

import math
import sys
import time
import traceback
from pathlib import Path

from base.connector import Connector
from base.testexception import TestException
from configuration.configuration import ConnectorTestConfiguration
from models.spec import TestCaseSpecification
from testspecs.account_test_case import AccountCheckTest
from testspecs.invoice_test_case import InvoiceCheckTest
from files.filebuilder import FileBuilder

# -------------------------------------------------------------------------------
#  Global Variables
# -------------------------------------------------------------------------------

configuration = ConnectorTestConfiguration()


# -------------------------------------------------------------------------------
#  Main Function
# -------------------------------------------------------------------------------


def main(spec_name: str, test_suite_directory: str):
    """
    This function is the main controller for test case generation.

    Arguments:
        product_spec_filename - the file name of the product spec
        test_suite_library - the directory that holds test suites
    """
    print("Starting test suite generation for: " + spec_name)
    prior = time.time()
    exit_code = 0
    try:
        generate(spec_name, test_suite_directory)
    except TestException as e:
        print("Error: " + str(e))
        info = sys.exc_info()
        tb = info[2]
        traceback.print_tb(tb)
        exit_code = 1
    except Exception as e:
        print("Exception: " + str(e))
        info = sys.exc_info()
        tb = info[2]
        traceback.print_tb(tb)
        exit_code = 1
    finally:
        now = time.time()
        duration = math.ceil(now - prior)
        print("Ending test case generation - " + str(duration) + " seconds")
    sys.exit(exit_code)


def generate(spec_name: str, test_suite_directory: str):
    """
    Validate the inputs for this test case and output the test cases.

    Arguments:
        spec_name - the name of the specification
        test_suite_directory - the parent directory that holds the project test cases.
    """
    #
    # Determine the specification to use
    #
    assert spec_name is not None, "Specification name must not be None"
    assert len(spec_name) > 0, "Specificaiton name must not be an empty string"
    spec = determine_spec(spec_name)
    output_directory = create_output_directory(spec, test_suite_directory)
    file_builder = FileBuilder(spec, output_directory, 1)
    file_builder.produce_test_case()
    return


def determine_spec(spec_name: str) -> TestCaseSpecification:
    """
    Return the test case specification to be used to generate the test cases.
    """
    if spec_name == "AccountCheckTest":
        cnx = Connector.create_connector(configuration.data_source, configuration.database)
        spec = AccountCheckTest(cnx)
        cnx.close()
    elif spec_name == "InvoiceCheckTest":
        cnx = Connector.create_connector(configuration.data_source, configuration.database)
        spec = InvoiceCheckTest(cnx)
        cnx.close()
    else:
        raise TestException("Unsupported test specification: " + spec_name)
    return spec


def create_output_directory(spec: TestCaseSpecification, test_suite_directory: str) -> str:
    """
    Create the full directory for the test suite.  It is the concatenation of:
    -- the test suite directory
    -- the project name
    -- the test suite name

    """
    validate_directory(test_suite_directory)
    full_path = spec.build_test_suite_directory(test_suite_directory)
    validate_directory(full_path)
    return full_path


def validate_directory(dir: str):
    """
    Check that the directory exists and is a directory.

    Arguments:
        dir - a directory path to be checked
    """
    path = Path(dir)
    if not path.is_dir():
        raise TestException("Path is not a directory: " + dir)
    return



# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------


if __name__ == '__main__':
    """
    Run the test generation program
    """
    if len(sys.argv) != 3:
        print("""
              To execute SuiteDreams, use this command:

              python main.py spec_name test_suite_directory
              """)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])