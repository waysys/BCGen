# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
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
__version__ = "03-Sep-2021"


"""
The test case module contains the TestCase class.
"""

from xml.dom import minidom
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from _datetime import date

from models.spec import TestCaseSpecification, TestTableSpecification
from models.testcasetable import ColumnTestTable


# -------------------------------------------------------------------------------
#  Test Case Class
# -------------------------------------------------------------------------------


class TestCase:
    """
    The TestCase class models an HTML elements used for GFIT test cases.
    The class creates the descriptive information at the beginning of the
    test case and calls a function in the test case table module to create
    the specific tables for this test case..
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, spec: TestCaseSpecification, num: int):
        """
        Initialize the class.

        Argument:
            spec - the test case specification for this test case.
            num - the differentiating number for this test case
        """
        assert spec is not None, "Test specification must not be None"
        assert num > 0, "Test case number must be positive, not: " + str(num)
        self._html: Element = Element("html")
        self._author: str = spec.author
        self._description: str = spec.description
        self._test_case_number: int = num
        self._spec: TestCaseSpecification = spec
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def title(self) -> str:
        """
        This property holds the content that goes into the <title> element in
        the heading.
        """
        assert self._spec.suite_name is not None, "Title must not be None"
        return self._spec.suite_name

    @property
    def project(self) -> str:
        """
        Return the name of the project.
        """
        assert self._spec.project_name is not None, "Project must not be None"
        return self._spec.project_name

    @property
    def author(self) -> str:
        """
        Return the author of this test case.
        """
        assert self._spec.author is not None, "Author must not be None"
        return self._spec.author

    @property
    def description(self) -> str:
        """
        Return a description of the test case.
        """
        assert self._spec.description is not None, "Description must not be None"
        return self._spec.description

    @property
    def test_case_number(self) -> str:
        """
        The four digit number associated with the test case being created.
        """
        result = str(self._test_case_number)
        while len(result) < 4:
            result = "0" + result
        return result

    # ---------------------------------------------------------------------------
    #  Element Creation Operations
    # ---------------------------------------------------------------------------

    def initialize(self) -> str:
        """
        Create the initial hierarchy of a test case file.
        """
        root = self.create_html()
        head = self.create_head()
        root.append(head)
        body = self.create_body()
        root.append(body)
        self._html = self.prettify(root)
        return self._html

    @staticmethod
    def create_html() -> Element:
        """
        Return an HTML element with the namespace defined

        Returns:
            HTML element
        """
        attrib = {
            "xmlns": "http://www.w3.org/1999/xhtml",
            "xml:lang": "en"
        }
        root = Element("html", attrib)
        return root

    def create_head(self) -> Element:
        """
        Return the head element.
        """
        head = Element("head")
        tle = Element("title")
        tle.text = self.title
        head.append(tle)
        style = TestCase.create_style()
        head.append(style)
        return head

    @staticmethod
    def create_style() -> Element:
        """
        Create the style element that defines the unique and claim number classes.
        """
        attrib = {
            "type": "text/css"
        }

        style = Element("style", attrib)
        css = """
              td.unique
              {
                color : red;
                font : bold
              }
              td.claimnumber
              {
                color : purple;
                font  : bold
              }
              """
        style.text = css
        return style

    def create_body(self) -> Element:
        """
        Create the body element
        """
        #
        # Create test case description
        #
        body = Element("body")
        test_description = self.create_test_description()
        body.append(test_description)
        hr = Element("hr")
        body.append(hr)
        self.create_test_tables(body)
        return body

    def create_test_tables(self, body: Element):
        """
        Create the test tables specific to this test case.

        Arguments:
            body - the body of the HTML page
            spec - the test specification
        """

        for table_spec in self._spec.tables:
            self.format_test_table(body, table_spec)
        return

    def format_test_table(self, body: Element, table_spec: TestTableSpecification):
        """
        Add the H2 heading and the test table to the body of test case.

        Arguments:
            body - the body of the test case
            table_spec - an instance of the test table specification
        """
        heading = self.create_heading(table_spec.heading)
        body.append(heading)
        table = ColumnTestTable(body, table_spec)
        element = table.create_table()
        body.append(element)
        return

    @staticmethod
    def create_heading(title):
        """
        Create an H2 heading with the title from the test table.
        """
        h2 = Element("h2")
        h2.text = title
        return h2

    def create_test_description(self) -> Element:
        """
        Create a description list element with information about the test case.
        """
        dl = Element("dl")
        TestCase.create_dl_dt(dl, "Project:", self.project)
        TestCase.create_dl_dt(dl, "Author:", self.author)
        a_date = str(date.today())
        TestCase.create_dl_dt(dl, "Date:", a_date)
        TestCase.create_dl_dt(dl, "Repeatable:", self._spec.repeatable)
        TestCase.create_dl_dt(dl, "Description:", self.description)
        return dl

    @staticmethod
    def create_dl_dt(dl, term: str, description: str):
        """
        Create a par of element (dt and dd) and append them to a dl element

        Arguments:
            dl - a dl element
            term - the content of the dt element
            description - the content of the dd element
        """
        dt = Element("dt")
        dt.text = term
        dd = Element("dd")
        dd.text = description
        dl.append(dt)
        dl.append(dd)
        return

    # ---------------------------------------------------------------------------
    #  Output Operations
    # ---------------------------------------------------------------------------

    @staticmethod
    def prettify(elem) -> str:
        """
        Return a pretty-printed XML string for the element elem.
        """
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def dump(self):
        """
        Output the file to standard out.
        """
        print(TestCase.prettify(self._html))
        return
