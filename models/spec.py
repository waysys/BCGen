# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "01-Sep-2021"

"""
This module specifies the format for defining the test case.
"""

# -------------------------------------------------------------------------------
#  Test Table Specification
# -------------------------------------------------------------------------------


class TestTableSpecification:
    """
    This class defines the specification of a test table.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize an instance of this class.
        """
        self.heading: str = ""
        self.fixture: str = ""
        self.columns: list[str] = []
        self.is_unique: list[bool] = []
        self.test_id_prefix = ""
        self.test_id_start = 10
        self.spec = None
        self.rows: list[list[str]] = []
        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def add_row(self, row: list[str]):
        """
        Add a test row to the test table.

        Arguments:
            row - a row of test values
        """
        assert row is not None, "row must not be None"
        assert self.columns is not None, "columns must not be None"
        assert len(self.columns) > 0, "Table columns must be set before adding rows"
        assert len(self.columns) == len(row), "Number of values in row does not equal number of columns"
        self.rows.append(row)
        return

    @property
    def number_rows(self):
        """
        The number of the row in the table.  The first row with data, after
        the fixture and headings, is number 1.
        """
        return len(self.rows) - 1

    @property
    def has_rows(self):
        """
        Return True if the table has at least one row of data.
        """
        return self.number_rows > 0

# -------------------------------------------------------------------------------
#  Test Case Specification
# -------------------------------------------------------------------------------


class TestCaseSpecification:
    """
    This class allows subclasses to specify the details for generating GFIT
    test cases.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Initialize an instance of this class.
        """
        self.project_name: str = ""
        self.application_name = "BC"
        self.suite_name: str = ""
        self.suite_id: str = ""
        self.description: str = ""
        self.version: str = ""
        self.author = ""
        self.repeatable = "Yes"
        self.seed: int = 67887
        self.tables: list[TestTableSpecification] = []
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def table_count(self) -> int:
        """
        Return the number of test table specifications in the test case specification.
        """
        return len(self.tables)

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def add_test_table(self, test_table: TestTableSpecification):
        """
        Add a test table specification to the test case specification.

        Arguments:
            test_table - an instance of the test table
        """
        assert test_table is not None, "test table must not be None"
        self.tables.append(test_table)
        test_table.spec = self
        return

    def build_test_suite_directory(self, test_suite_directory):
        """
        Construct the full test suite directory consisting of:
        -- the test suite directory
        -- the project name
        -- the test suite name

        Arguments:
            test_suite_directory - the path that points to a directory with
               subdirectories for projects.
        """
        full_path = test_suite_directory + "/"
        full_path += self.application_name + "/"
        full_path += self.project_name + "/"
        full_path += self.suite_name
        return full_path
