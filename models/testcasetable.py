# -------------------------------------------------------------------------------
#
#  Copyright (c) 2020 Waysys LLC
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
__version__ = "30-Dec-2020"

"""
This module models a test case table.  The first row of the table is the fixture path.
If the fixture is a column fixture, the second row of the table contains the 
column headings.  If the fixture is an action fixture, there is no row of column headings.
The remaining rows contain the test data.
"""

from xml.etree.ElementTree import Element


# -------------------------------------------------------------------------------
#  Create test tables operation
# -------------------------------------------------------------------------------


def create_test_tables(body, product_spec, test_case_number):
    """
    Create the test tables specific to this test case.

    Arguments:
        body - the body of the HTML page
        product_spec - the product specification table
        test_case_number - the test case number
    """
    tables = [
        CreateSubmissionTestTable(body, product_spec, test_case_number),
        AnswerQuestionsTestTable(body, product_spec, test_case_number),
        UpdateDwellingTestTable(body, product_spec, test_case_number),
        CreateCoveragesTestTable(body, product_spec, test_case_number),
        QuiteIssueTestTable(body, product_spec, test_case_number)
    ]

    for table in tables:
        format_test_table(body, table)
    return


def format_test_table(body, table):
    """
    Add the H2 heading and the test table to the body of test case.

    Arguments:
        body - the body of the test case
        table - an instance of the test table
    """
    heading = create_heading(table.title)
    body.append(heading)
    element = table.create_test_table()
    body.append(element)
    return


def create_heading(title):
    """
    Create an H2 heading with the title from the test table.
    """
    h2 = Element("h2")
    h2.text = title
    return h2


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

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize the instance of this class.

        Arguments:
            body - the HTML body element
            product_spec - product specification
            test_case_number - a string with 4 digits indicating the
        """
        assert body is not None, "Test case body must not be None"
        assert product_spec is not None, "Product specification must not be None"
        assert test_case_number is not None, "Test case number must not be None"
        # fixture set in subclasses
        self._fixture = None
        self._rows = []
        self._body = body
        self._table = None
        self._title = None
        self._num = 0
        self._product_spec = product_spec
        self._test_case_number = test_case_number
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
        suiteid = self._product_spec.suite_id
        return suiteid

    @property
    def fixture(self):
        """
        The full path of the fixture.
        """
        assert self._fixture is not None, "fixture has not been set."
        return self._fixture

    @fixture.setter
    def fixture(self, package):
        """
        Set the full package of the fixture.
        """
        assert package is not None, "fixture package must not be None"
        self._fixture = package
        return

    @property
    def title(self):
        """
        The text that goes in an H2 element describing a table.
        """
        assert self._title is not None, "Title has not been set"
        return self._title

    @title.setter
    def title(self, text):
        """
        Argument:
            text - the text of the title
        """
        assert text is not None, "title must not be None"
        self._title = text
        return

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
    def test_id(self):
        """
        Return the test id for this test
        """
        testid = "TEST-" + self.public_id
        return testid

    @property
    def public_id(self):
        """
        Return the value of the public id
        """
        publicid = self.suite_id + "-" + self.test_case_number + "-" + \
            self.role_abbreviation
        return publicid

    @property
    def submission_id(self):
        """
        Return a public id for the submission.  This value must be the same throughout
        the test case but must be unique to the test case.
        """
        submission_id = "SUBMISSION-" + self.test_case_number
        return submission_id

    @property
    def test_case_number(self):
        """
        4 digit code uniquely identify this test case.
        """
        return self._test_case_number

    @property
    def role(self):
        """
        Return the role this table plays.
        """
        assert self._role is not None, "Role has not been set"
        return self._role

    @role.setter
    def role(self, role):
        """
        Set the role for this table.

        Arguments:
            role - the role for this table.  See the Suite Dreams schema for values.
        """
        assert role is not None, "Role must not be None"
        assert len(role) > 0, "Role must not be an empty string"
        self._role = role
        return

    @property
    def role_abbreviation(self):
        """
        A two letter abbreviation identifying unique to the role.
        """
        assert self._role_abbreviation is not None, "Role abbreviation must not be None"
        return self._role_abbreviation

    @role_abbreviation.setter
    def role_abbreviation(self, value):
        """
        Set the role abbreviation.

        Arguments:
            value - the two leter abbreviation for the role
        """
        assert value is not None, "Role abbreviation must not be None"
        assert len(value) == 2, "Invalid value for role abbreviation: " + value
        self._role_abbreviation = value

    @property
    def attribute(self):
        """
        Return the dictionary holding the class attribute.
        """
        return self._attribute

    @property
    def product_spec(self):
        """
        Return the product specification instance.
        """
        return self._product_spec

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_table(self):
        """Create heading and a table element"""
        attrib = {"border": "1"}
        self._table = Element("table", attrib)
        return

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

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
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


# -------------------------------------------------------------------------------
#  Create submission test table
# -------------------------------------------------------------------------------


class CreateSubmissionTestTable(ColumnTestTable):
    """
    This class generates the create submission table.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
        self.title = "Create Submission"
        self.role = "CreateSubmission"
        self.role_abbreviation = "CS"
        self.fixture = product_spec.fetch_fixture(self.role)
        assert self.fixture is not None, "Unable to retrieve fixture for role: " + self.role
        self.headings = [
            "TestId",
            "Submission ID",
            "Account Number",
            "Submission Date",
            "Valid()"
        ]
        self.is_unique = [
            False,
            True,
            False,
            False,
            False
        ]
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def account_number(self):
        """
        Fetch the account number from the product specification.
        """
        acct_num = self.product_spec.account_number
        assert acct_num is not None, "Account number was not found under Policy"
        return acct_num

    @property
    def submission_date(self):
        """
        Fetch the submission date from the product specification.
        If it is not found in the product specification, use the current date.
        """
        date = self.product_spec.submission_date
        return date

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_test_table(self):
        """
        Create the table html for the create submission table.
        """
        self.create_table()
        self.add_fixture()
        self.add_row(self.headings, self.is_unique)
        self.add_row(self.create_values(), None)
        return self.table

    def create_values(self):
        """
        Create a list of values.
        """
        values = [
            self.test_id + "-" + str(self.row_number),
            self.submission_id,
            self.account_number,
            self.submission_date,
            "true"
        ]
        return values


# -------------------------------------------------------------------------------
#  Answer questions test table
# -------------------------------------------------------------------------------


class AnswerQuestionsTestTable(ColumnTestTable):
    """
    This class generates the table to create answers to underwriting
    questions.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
        self.title = "Create Answers to Pre-Qualificaton Questions"
        self.role = "AnswerQuestions"
        self.role_abbreviation = "AQ"
        self.fixture = product_spec.fetch_fixture(self.role)
        assert self.fixture is not None, "Unable to retrieve fixture for role: " + self.role
        self.headings = [
            "TestId",
            "Submission ID",
            "Question Set Code",
            "Question Code",
            "Answer",
            "Valid()"
        ]
        self.is_unique = [
            False,
            True,
            False,
            False,
            False,
            False
        ]
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_test_table(self):
        """
        Create the table html for the create submission table.
        """
        self.create_table()
        self.add_fixture()
        self.add_row(self.headings, self.is_unique)
        self.create_rows()
        return self.table

    def create_rows(self):
        """
        Create the rows in the table.

        Note: questions do not have weights for selection.
        """
        question_set_elements = self.product_spec.fetch_question_sets()
        for question_set_element in question_set_elements:
            self.process_question_set(question_set_element)
        return

    def process_question_set(self, question_set_element):
        """
        Output the rows for a single question set.

        Arguments:
            question_set_element - the element for the question set that
               contains questions
        """
        question_set_code = self.product_spec.fetch_question_set_code(question_set_element)
        question_elements = self.product_spec.fetch_questions(question_set_element)
        for question_element in question_elements:
            row = self.create_values(question_set_code, question_element)
            self.add_row(row, None)
        return

    def create_values(self, question_set_code, question):
        """
        Create the values for a row.

        Arguments:
            question_set_code - the question set code
            question - a question element
        """
        (question_code, answer) = self.product_spec.fetch_question_code_and_answer(question)
        values = [
            self.test_id + "-" + str(self.row_number),
            self.submission_id,
            question_set_code,
            question_code,
            answer,
            "true"
        ]
        return values


# -------------------------------------------------------------------------------
#  Update dwelling test table
# -------------------------------------------------------------------------------


class UpdateDwellingTestTable(ColumnTestTable):
    """
    This class creates the test table for updating the dwelling.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
        self.title = "Update Dwelling"
        self.role = "UpdateDwelling"
        self.role_abbreviation = "UD"
        self.fixture = product_spec.fetch_fixture(self.role)
        assert self.fixture is not None, "Unable to retrieve fixture for role: " + self.role
        self.headings = [
            "TestId",
            "Submission ID"
        ]
        self.is_unique = [
            False,
            True
        ]
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_test_table(self):
        """
        Create the table html for the create submission table.
        """
        self.create_table()
        self.add_fixture()
        self.update_headings()
        self.add_row(self.headings, self.is_unique)
        self.create_row()
        return self.table

    def update_headings(self):
        """
        Add the additional properties to the heading array.  Also add False
        to the is_unique array so it is the same size as the heading array.
        """
        coverable_element = self.fetch_dwelling()
        headings = self.product_spec.fetch_property_headings(coverable_element)
        for heading in headings:
            self.headings.append(heading)
            self.is_unique.append(False)
        self.headings.append("Valid()")
        self.is_unique.append(False)
        return

    def fetch_dwelling(self):
        """
        Return the coverable element for dwelling.
        """
        result = None
        root_element = self.product_spec.root_element
        product_element = self.product_spec.fetch_element(root_element, "Product")
        coverable_elements = self.product_spec.fetch_all_elements(product_element, "Coverable")
        for coverable in coverable_elements:
            coverable_name = self.product_spec.fetch_text(coverable, "CoverableName")
            if coverable_name == "HOPDwelling":
                result = coverable
                break
        return result

    def create_row(self):
        """
        Create the rows in the table
        """
        coverable_element = self.fetch_dwelling()
        property_values = self.product_spec.fetch_property_values(coverable_element)
        row = [
            self.test_id,
            self.submission_id
        ]
        for value in property_values:
            row.append(value)
        row.append("true")
        self.add_row(row, None)
        return


# -------------------------------------------------------------------------------
#  Quote and Issue Test Table
# -------------------------------------------------------------------------------


class QuiteIssueTestTable(ColumnTestTable):

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
        self.title = "Quote and Issue"
        self.role = "QuoteIssue"
        self.role_abbreviation = "QI"
        self.fixture = product_spec.fetch_fixture(self.role)
        assert self.fixture is not None, "Unable to retrieve fixture for role: " + self.role
        self.headings = [
            "TestId",
            "Submission ID",
            "Quote()",
            "Issue()"
        ]
        self.is_unique = [
            False,
            True,
            False,
            False
        ]
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_test_table(self):
        """
        Create the table html for the create submission table.
        """
        self.create_table()
        self.add_fixture()
        self.add_row(self.headings, self.is_unique)
        self.create_row()
        return self.table

    def create_row(self):
        """
        Create the rows in the table
        """
        row = [
            self.test_id,
            self.submission_id,
            "true",
            "true"
        ]
        self.add_row(row, None)
        return

# -------------------------------------------------------------------------------
#  Action fixture test table
# -------------------------------------------------------------------------------


class ActionTestTable(TestTable):
    """
    This class models the test table for an action fixture.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def set_property(self, property_name, property_value, unique):
        """
        Add a row to the fixture to set a property.

        Arguments:
            property_name - the name of the property to be set
            property_value - the value for the property
            unique - True if the "set" value should have a class of unique
        """
        assert property_name is not None, "Property name must not be None"
        assert len(property_name) > 0, "Property name must not be empty"
        assert property_value is not None, "Property value must not be None"
        assert len(property_value) > 0, "Property value must not be empty"
        row = [
            "set",
            property_name,
            property_value,
            ""
        ]
        is_unique = [
            unique,
            False,
            False,
            False
        ]
        self.add_row(row, is_unique)
        return

    def select_submission(self):
        """
        Create a row 'select submission submission_id'
        """
        row = [
            "select",
            "submission",
            self.submission_id,
            ""
        ]
        is_unique = [
            True,
            False,
            False,
            False
        ]
        self.add_row(row, is_unique)
        return

    def select_coverable(self, coverable_name):
        """
        Create a row to select the coverable.

        Arguments:
            coverable_name - the coverable name
        """
        assert coverable_name is not None, "Coverable name must not be None"
        assert len(coverable_name) > 0, "Coverable name must not be empty"
        row = [
            "select",
            "coverable",
            coverable_name,
            ""
        ]
        self.add_row(row, None)
        return

    def create_coverage(self, coverage_code, coverage_count):
        """
        Create a row to create the coverage.

        Arguments:
            coverage_code - the code identifier for the coverage
            coverage_count - the number of this coverage in the table.
        """
        assert coverage_code is not None, "Coverage name must not be None"
        assert len(coverage_code) > 0, "Coverage name must not be empty"
        row = [
            "create",
            "coverage",
            self.test_id + "-" + str(coverage_count),
            coverage_code
        ]
        self.add_row(row, None)
        return

    def add_with(self, coverage_term_code, term_value):
        """
        Create a row with the 'with' command.

        Arguments:
            coverage_term_code - the code for the coverage term
            term_value - the value for the coverage term
        """
        row = [
            "with",
            coverage_term_code,
            term_value,
            ""
        ]
        self.add_row(row, None)
        return

    def commit(self):
        """
        Create a row with the 'commit' command.
        """
        row = [
            "commit",
            "",
            "",
            ""
        ]
        self.add_row(row, None)
        return


# -------------------------------------------------------------------------------
#  Create Coverages Test Table
# -------------------------------------------------------------------------------


class CreateCoveragesTestTable(ActionTestTable):
    """
    This class creates coverages.  It uses the action fixture.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, body, product_spec, test_case_number):
        """
        Initialize this instance of this class.
        """
        super().__init__(body, product_spec, test_case_number)
        self.title = "Create Coverages"
        self.role = "CreateCoverages"
        self.role_abbreviation = "CC"
        self.fixture = product_spec.fetch_fixture(self.role)
        self.coverage_count = 0
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def create_test_table(self):
        """
        Create the 'create coverage' test table.
        """
        #
        # Create the table
        #
        self.create_table()
        self.add_fixture()
        #
        # Set the test id
        #
        self.set_property("TestId", self.test_id, False)
        #
        # Select the submission
        #
        self.select_submission()
        #
        # Create rows for each coverable
        #
        self.coverage_count = 0
        coverable_elements = self.product_spec.fetch_coverables()
        assert len(coverable_elements) > 0, "Product must have at least one coverable"
        for coverable_element in coverable_elements:
            self.process_coverables(coverable_element)
        self.commit()
        return self.table

    def process_coverables(self, coverable_element):
        """
        Generate the rows a coverable including the coverages

        Arguments:
            coverable_element - the element for a coverable
        """
        #
        # Select the coverable
        #
        coverable_name = self.product_spec.fetch_text(coverable_element, "CoverableName")
        self.select_coverable(coverable_name)
        #
        # Process selected coverages
        #
        coverage_elements = self.product_spec.fetch_coverages(coverable_element)
        assert len(coverage_elements) > 0, "Coverable must have coverages: " + coverable_name
        for coverage_element in coverage_elements:
            self.process_coverage(coverage_element)
        return

    def process_coverage(self, coverage_element):
        """
        Generate rows for coverages.

        Arguments:
            coverage_element - a coverage element
        """
        #
        # Create the coverage
        #
        self.coverage_count += 1
        coverage_code = self.product_spec.fetch_coverage_code(coverage_element)
        self.create_coverage(coverage_code, self.coverage_count)
        #
        # Add the coverage terms
        #
        cov_term_elements = self.product_spec.fetch_coverage_terms(coverage_element)
        for cov_term_element in cov_term_elements:
            self.process_coverage_term(cov_term_element)
        return

    def process_coverage_term(self, cov_term_element):
        """
        Generate a row for a coverage term.

        Arguments:
            term_element - a coverage term element
        """
        coverage_term_code = self.product_spec.fetch_text(cov_term_element, "CoverageTermCode")
        term_value = self.product_spec.fetch_coverage_term_value(cov_term_element)
        assert term_value is not None, "Term value must not be None for coverage term: " + \
                                       coverage_term_code
        assert len(term_value) > 0, "Term value must not be empty for coverage term: " + \
                                    coverage_term_code
        self.add_with(coverage_term_code, term_value)
        return
