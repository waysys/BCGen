# -------------------------------------------------------------------------------
#
#  Copyright (c) 2018 Waysys LLC
#
# -------------------------------------------------------------------------------
#
#  Waysys LLC MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE SUITABILITY OF
#  THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
#  TO THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE, OR NON-INFRINGEMENT. CastleBay SHALL NOT BE LIABLE FOR
#  ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT OF USING, MODIFYING OR
#  DISTRIBUTING THIS SOFTWARE OR ITS DERIVATIVES.
#
# For further information, contact wshaffer@waysysweb.com
#
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "31-Dec-2020"

"""
This module holds the FileBuilder class. 
"""

from base.testexception import TestException
from models.testcase import TestCase
from models.spec import TestCaseSpecification

# -------------------------------------------------------------------------------
#  FileBuilder class
# -------------------------------------------------------------------------------


class FileBuilder:
    """
    The File Builder class creates a single test case file in HTML format.  It is the
    intermediate between the main module, the test specification, and the test case.
    The main role of this class is to handle the input/output for the test case.
    """

    def __init__(self, spec: TestCaseSpecification, test_suite_library: str, num: int):
        """
        Initialize this class.

        Arguments:
            test_suite_library - the directory where the test suite will be placed
        """
        assert spec is not None, "FileBuilder: Test specification must not be None"
        assert test_suite_library is not None, "FileBuilder: test suite library must not be null"
        assert len(test_suite_library) > 0, "FileBuilder: test suit library must not be empty"
        assert num > 0, "Test case number must be greater than 0, not - " + str(num)
        self._spec = spec
        self._test_suite_library = test_suite_library
        self._num = num
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def test_suite_library(self) -> str:
        """
        Return the name of the directory that will hold the test suite directory
        """
        return self._test_suite_library

    @property
    def suite_name(self) -> str:
        """
        Return the name for the test suite
        """
        name = self._spec.suite_name
        return name

    @property
    def test_suite_dir(self) -> str:
        """
        Return the directory path where the test case files will reside.
        """
        direct = self.test_suite_library + "/" + self.suite_name
        return direct

    @property
    def test_case_number(self) -> str:
        """
        Return the number of this test case as a string with 4 digits.
        """
        value = str(self._num)
        while len(value) < 4:
            value = "0" + value
        return value

    @property
    def suite_id(self) -> str:
        """
        Return the suite id
        """
        return self._spec.suite_id

    @property
    def test_case_filename(self):
        """
        Return the full path name of the test case file.
        """
        name = self.test_suite_dir + "/" + self.test_case_number + "_" + self.suite_id + ".html"
        return name

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def produce_test_case(self):
        """
        Generate a test case file in the test suite directory.
        """
        test_case = TestCase(self._spec)
        html = test_case.initialize()
        self.output(html)
        return

    def output(self, html):
        """
        Output the HTML to its file.
        """
        file = None
        try:
            file = open(self.test_case_filename, 'w')
            file.write(html)
        except Exception as e:
            raise TestException(e)
        finally:
            if file is not None:
                file.close()
        return
