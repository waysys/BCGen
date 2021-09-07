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
__version__ = "2021-09-04"

"""
This module models a test case table.  The first row of the table is the fixture path.
If the fixture is a column fixture, the second row of the table contains the 
column headings.  If the fixture is an action fixture, there is no row of column headings.
The remaining rows contain the test data.
"""

from xml.etree.ElementTree import Element

from models.spec import TestTableSpecification

# -------------------------------------------------------------------------------
#  Test table class
# -------------------------------------------------------------------------------


class TestTable:
    """
    This class is the parent of the various types of tables.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, table_spec: TestTableSpecification):
        """
        Initialize the instance of this class.

        Arguments:
            body - the HTML body element
            table_spec - the specification for the table
        """
        assert body is not None, "Test case body must not be None"
        assert table_spec is not None, "Product specification must not be None"
        # fixture set in subclasses
        self._table_spec = table_spec
        self._fixture = None
        self._rows = []
        self._body = body
        self._table = None
        self._title = None
        self._num = 0
        self._role = None
        self._role_abbreviation = None
        self._attribute = {"class": "unique"}
        self._submission_id = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def suite_id(self):
        """
        Return the suite id
        """
        suiteid = self._table_spec.spec.suite_id
        return suiteid

    @property
    def fixture(self):
        """
        The full path of the fixture.
        """
        assert self._fixture is not None, "fixture has not been set."
        return self._fixture

    @property
    def title(self):
        """
        The text that goes in an H2 element describing a table.
        """
        assert self._title is not None, "Title has not been set"
        return self._title

    @property
    def body(self):
        """
        The HTML body of the test case
        """
        return self._body

    @property
    def table(self):
        """
        The table being worked on.
        """
        assert self._table is not None, "Table has not been created"
        return self._table

    @property
    def attribute(self):
        """
        Return the dictionary holding the class attribute.
        """
        return self._attribute

    @property
    def table_spec(self):
        """
        Return the product specification instance.
        """
        return self._table_spec

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_table(self):
        """Create heading and a table element"""
        attrib = {"border": "1"}
        self._table = Element("table", attrib)
        return self._table

    def add_row(self, values, is_unique):
        """
        Add a row to the table in the test case.

        Argument:
            values - a list of strings for the content of the row
            is_unique - a list of booleans.  Entry is True if the corresponding value should be unique.
              This parameter can be None, if there are not unique column settings.
        """
        assert values is not None, "Values must not be None"
        assert len(values) > 0, "add_row: there must be at least one value in a row"

        if is_unique is not None:
            assert len(values) == len(is_unique), \
                "Length of is_unique list " + str(len(is_unique)) + " must equal length of values list " + \
                str(len(values))
        tr = Element("tr")
        index = 0
        for value in values:
            if (is_unique is not None) and is_unique[index]:
                td = Element("td", self.attribute)
            else:
                td = Element("td")
            td.text = value
            tr.append(td)
            index += 1
        self.table.append(tr)
        return

    def add_fixture(self):
        """
        Add the fixture to the table.
        """
        row = [self.fixture]
        self.add_row(row, None)
        return


# -------------------------------------------------------------------------------
#  Column fixture test table
# -------------------------------------------------------------------------------


class ColumnTestTable(TestTable):
    """
    This class models the test table for column fixtures.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, table_spec: TestTableSpecification):
        """
        Initialize this instance of this class.

        Arguments:
            body -
        """
        super().__init__(body, table_spec)
        self._headings = []
        # set the row number to -1 to account for the fixture and heading rows.
        # Row 1 should be the first row of data.
        self._row_number = -1
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def headings(self):
        """
        The headings row on a column fixture.
        """
        return self._headings

    @headings.setter
    def headings(self, row):
        """
        Set the headings property to the string array row.

        Arguments:
            row - an array of strings representing the column properties
        """
        assert row is not None, "Headings must not be None"
        assert len(row) > 0, "Headings must not be empty"
        self._headings = row
        return

    @property
    def row_number(self):
        """
        The number of the row in the table.  The first row with data, after
        the fixture and headings, is number 1.
        """
        return self._row_number

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def add_row(self, values, is_unqiue):
        """
        Overriding add_row in super class to increment row number.
        """
        super().add_row(values, is_unqiue)
        self._row_number += 1
        return
