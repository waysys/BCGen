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
The test case module contains the TestCase class.
"""

from xml.dom import minidom
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from _datetime import date

from testcasetable import create_test_tables


# -------------------------------------------------------------------------------
#  Test Case Class
# -------------------------------------------------------------------------------


class TestCase:
    """
    The TestCase class models an HTML elements used for GFIT test cases.
    The class creates the descriptive information at the beginning of the
    test case and calls a function in the testcasetable module to create
    the specific tables for this test case..
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, test_case_number: str):
        """
        Initialize the class.

        Argument:
            test_case_number
        """
        self._html = None
        self._title = self.product_spec.suite_name
        self._project = self.product_spec.project
        self._author = self.product_spec.author
        self._description = self.product_spec.description
        self._test_case_number = test_case_number
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def title(self):
        """
        This property holds the content that goes into the <title> element in
        the heading.
        """
        assert self._title is not None, "Title must not be None"
        return self._title

    @property
    def project(self):
        """
        Return the name of the project.
        """
        assert self._project is not None, "Project must not be None"
        return self._project

    @property
    def author(self):
        """
        Return the author of this test case.
        """
        assert self._author is not None, "Author must not be None"
        return self._author

    @property
    def description(self):
        """
        Return a description of the test case.
        """
        assert self._description is not None, "Description must not be None"
        return self._description

    @property
    def product_spec(self):
        """Return the parsed XML product specification.
        """
        assert self._product_spec is not None, "Product specification has not been set"
        return self._product_spec

    @property
    def test_case_number(self):
        """
        The four digit number associated with the test case being created.
        """
        return self._test_case_number

    # ---------------------------------------------------------------------------
    #  Element Creation Operations
    # ---------------------------------------------------------------------------

    def initialize(self):
        """
        Create the initial hierarchy of a test case file.
        """
        root = TestCase.create_html()
        head = self.create_head()
        root.append(head)
        body = self.create_body()
        root.append(body)
        self._html = self.prettify(root)
        return self._html

    @staticmethod
    def create_html():
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

    def create_head(self):
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
    def create_style():
        """
        Create the style element that defines the unique and claimnumber classes.
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

    def create_body(self):
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
        create_test_tables(body, self.product_spec, self.test_case_number)
        return body

    def create_test_description(self):
        """
        Create a description list element with information about the test case.
        """
        dl = Element("dl")
        TestCase.create_dl_dt(dl, "Project:", self.project)
        TestCase.create_dl_dt(dl, "Author:", self.author)
        adate = str(date.today())
        TestCase.create_dl_dt(dl, "Date:", adate)
        TestCase.create_dl_dt(dl, "Repeatable:", "Yes")
        TestCase.create_dl_dt(dl, "Description:", self.description)
        return dl

    @staticmethod
    def create_dl_dt(dl, term, description):
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
    def prettify(elem):
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
