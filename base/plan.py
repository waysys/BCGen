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
This module defines classes that support the definition of environments, test projects,
and other information related to a development project.

When defining directories, do not end the path with / or \\.
"""

import os

from pyodbc import Error

from base.connector import Connector


# -------------------------------------------------------------------------------
#  Product Spec
# -------------------------------------------------------------------------------


class ProductSpec:
    """This class describes a product specification.  A product spec describes the
    features of a policy or claim.  Product specifications are particular to
    an application type.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, application_type):
        """
        Configure an instance of this class.

        Arguments:
            application_type - the type of application associated with this spec
        """
        assert application_type is not None, "Application type must not be None"
        self.application_type = application_type
        self.product_spec_name = None
        self.product_spec_description = ""
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def product_spec_dir(self) -> str:
        """
        Return the full path of the directory containing the product spec.
        """
        base_dir = self.application_type.project.product_spec_base_dir
        application_name = self.application_type.application_type_name
        diry = base_dir + "/" + application_name
        return diry

    @property
    def product_spec_file(self) -> str:
        """
        Return the full path of the product spec file.
        """
        path = self.product_spec_dir + "/" + self.product_spec_name + ".xml"
        return path

    @property
    def is_product_spec_file_valid(self) -> bool:
        """
        Return True if the product spec file exists.
        """
        result = os.path.isfile(self.product_spec_file)
        return result


# -------------------------------------------------------------------------------
#  Application Type
# -------------------------------------------------------------------------------


class ApplicationType:
    """
    The application type describes a type of application like PolicyCenter
    or ClaimCenter.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, project):
        """
        Configure an instance of this class.

        Arguments:
            project - the project associated with this type of application.
        """
        assert project is not None, "Environment must ot be None"
        self.project = project
        self.application_type_name = None
        self.application_type_description = ""
        self.product_specs: dict[str, ProductSpec] = {}
        return

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def has_product_spec(self, name: str) -> bool:
        """
        Return true if the application type has a product spec with the specified name.

        Arguments:
            name - the name of the product spec
        """
        assert name is not None, "Name must not be None"
        assert len(name) > 0, "Name must not be an empty string"
        return name in self.product_specs

    def create_product_spec(self, name: str) -> ProductSpec:
        """
        Return a new product spec with the specified name.

        Arguments:
            name - the name of the product spec
        """
        assert not self.has_product_spec(name), "Product spec already exists: " + name
        product_spec = ProductSpec(self)
        product_spec.product_spec_name = name
        self.product_specs[name] = product_spec
        return product_spec

    def fetch_product_spec(self, name: str) -> ProductSpec:
        """
        Return an existing product spec with the specified name.


        Arguments:
            name - the name of the product spec
        """
        assert self.has_product_spec(name), "Product spec does not exist: " + name
        return self.product_specs[name]


# -------------------------------------------------------------------------------
#  Application
# -------------------------------------------------------------------------------


class Application:
    """
    An application is a system with components like a database and web service.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, environment):
        """
        Configure an instance of this class.

        Arguments:
            environment - the environment that holds this application
        """
        assert environment is not None, "Environment must ot be None"
        self.environment = environment
        self.application_type = None
        self.application_description = ""
        self.database = None
        self.web_service = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def is_database_valid(self) -> bool:
        """
        Return True if the database definition for this application is a valid
        definition.
        """
        if self.database is None:
            result = False
        else:
            cnx = None
            try:
                cnx = Connector.create_connector(self.database)
                cursor = cnx.cursor()
                result = cursor.rowcount == -1
            except Error:
                result = False
            finally:
                if cnx is not None:
                    cnx.close()
        return result

    @property
    def application_name(self) -> str:
        """
        Return the name of the application.
        """
        assert self.application_type is not None, "Application type has not been set"
        return self.application_type.application_type_name


# -------------------------------------------------------------------------------
#  Environment
# -------------------------------------------------------------------------------


class Environment:
    """
    An environment is a representation of a collection of applications that
    function together.  Typical environments include production and test.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, project):
        """
        Configure the instance of this class.

        Arguments:
            project - the project that owns this environment
        """
        assert project is not None, "Project must not be None"
        self.env_name = "Environment"
        self.env_description = "Complete this property"
        self.applications: dict[Application] = {}
        self.test_output_base_dir = None
        self.project = project
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def is_output_base_dir_valid(self) -> bool:
        """
        Return True if the test output base directory exists.
        """
        if self.test_output_base_dir is None:
            result = False
        else:
            result = os.path.isdir(self.test_output_base_dir)
        return result

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def form_test_output_dir(self, test_group: str):
        """
        Return the full path to the directory that will hold the test output
        to the report.

        Arguments:
            test_group - the name of the test group being run
        """
        assert test_group is not None, "Test group must not be None"
        assert len(test_group) > 0, "Test group must not be an empty string"
        assert self.test_output_base_dir is not None, "Output base directory is not set"
        path = self.test_output_base_dir + "/" + self.env_name + "/" + test_group
        return path

    def is_output_dir_valid(self, test_group: str):
        """
        Return True if the output directory exists.
        """
        path = self.form_test_output_dir(test_group)
        return os.path.isdir(path)

    def has_application(self, name: str) -> bool:
        """
        Return True if the environment has the application.

        Arguments:
            name - the name of the application
        """
        assert name is not None, "Name must not be None"
        assert len(name) > 0, "Name must not be empty string"
        return name in self.applications

    def create_application(self, name) -> Application:
        """
        Create a new application with the specified name.

        Arguments:
            name - the name of the application
        """
        assert not self.has_application(name), "This application already exists: " + name
        application = Application(self)
        application_type = self.project.fetch_application_type(name)
        application.application_type = application_type
        self.applications[name] = application
        return application

    def fetch_application(self, name):
        """
        Return the application with the specified name.

        Arguments:
            name - the name of the application
        """
        assert self.has_application(name), "Environment does not have this application: " + name
        return self.applications[name]


# -------------------------------------------------------------------------------
#  Test Suite
# -------------------------------------------------------------------------------


class TestSuite:
    """
    A test suite is a collection of test cases.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, test_group):
        """
        Initialize an instance of this class.
        """
        assert test_group is not None, "Test group must not be None"
        self.test_group = test_group
        self.test_suite_name = ""
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def test_suite_dir(self) -> str:
        """
        Return the full path to the test suite directory holding the test
        cases for the test suite.
        """
        path = self.test_group.test_group_base_dir + "/" + self.test_suite_name
        return path

    @property
    def is_test_suite_dir_valid(self) -> bool:
        """
        Return True if the test suite directory exists.
        """
        diry = self.test_suite_dir
        if diry is None:
            result = False
        else:
            result = os.path.isdir(diry)
        return result

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def test_suite_output(self, env_name: str) -> str:
        """
        Return the full path plus the file name of the output for the
        test suite.
        """
        environment: Environment = self.test_group.project.fetch_environment(env_name)
        output_path = environment.form_test_output_dir(self.test_group.test_group_name)
        assert environment.is_output_dir_valid(self.test_group.test_group_name), \
            "Suite output directory does not exist: " + output_path
        output = output_path + "/" + self.test_suite_name
        return output


# -------------------------------------------------------------------------------
#  Test Group
# -------------------------------------------------------------------------------


class TestGroup:
    """
    A test group is a set of test suites that are run together.  In Jenkins, test groups
    are called builds or projects.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, project):
        """
        Initialize an instance of this group.
        """
        assert project is not None, "Project must not be None"
        self.project = project
        self.test_group_name = None
        self.test_group_description = "Complete this property"
        self.test_suites: dict[str, TestSuite] = {}
        self.application_type = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def test_group_base_dir(self) -> str:
        """
        Form the base directory where the test group has test suite directories.
        """
        assert self.project.test_suite_base_dir is not None, "Test suite base directory is not set"
        assert self.application_type is not None, "Application has not been set"
        assert self.application_type.application_type_name is not None, "Application type name has not been set"
        assert self.test_group_name is not None, "Test group name has not been set"
        diry = self.project.test_suite_base_dir + "/"
        diry += self.application_type.application_type_name + "/"
        diry += self.test_group_name
        return diry

    @property
    def is_test_group_base_dir_valid(self) -> bool:
        """
        Return True if the test group base directory exists.
        """
        path = self.test_group_base_dir
        return os.path.isdir(path)

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def has_test_suite(self, name: str) -> bool:
        """
        Return True is the test group already has a test suite with the specified name.

        Arguments:
            name - the nae of the test suite
        """
        assert name is not None, "Name must not be None"
        assert len(name) > 0, "Name must not be empty string"
        return name in self.test_suites

    def create_test_suite(self, name: str) -> TestSuite:
        """
        Return a new test suite with the specified name.  Add the test suite to the dictionary
        of test suites.

        Arguments:
            name - the name of the test suite
        """
        assert not self.has_test_suite(name)
        test_suite = TestSuite(self)
        test_suite.test_suite_name = name
        self.test_suites[name] = test_suite
        return test_suite

    def fetch_test_suite(self, name: str) -> TestSuite:
        """
        Return the test suite with the specified name.  There must be a test suite with that name.

        Arguments:
            name - the name of the test suite
        """
        assert self.has_test_suite(name), "Test group does not have test suite: " + name
        return self.test_suites[name]


# -------------------------------------------------------------------------------
#  Project
# -------------------------------------------------------------------------------


class Project:
    """
    This class is the top level class.  Instances of this class hold instances
    of other plan classes.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self):
        """
        Configure the instance of this class.
        """
        self.project_name = ""
        self.project_description = ""
        self.environments: dict[str, Environment] = {}
        self.test_groups: dict[str, TestGroup] = {}
        self.application_types: dict[str, ApplicationType] = {}
        self.test_suite_base_dir = None
        self.product_spec_base_dir = None
        return

    # ---------------------------------------------------------------------------
    #  Properties
    # ---------------------------------------------------------------------------

    @property
    def is_base_dir_valid(self) -> bool:
        """
        Return True if the test suite base dir is an existing directory.
        """
        if self.test_suite_base_dir is None:
            result = False
        else:
            result = os.path.isdir(self.test_suite_base_dir)
        return result

    @property
    def is_product_spec_dir_valid(self) -> bool:
        """
        Return true if the product spec directory exists.
        """
        if self.product_spec_base_dir is None:
            result = False
        else:
            result = os.path.isdir(self.product_spec_base_dir)
        return result

    # ---------------------------------------------------------------------------
    #  Operations
    # ---------------------------------------------------------------------------

    def has_test_group(self, name: str) -> bool:
        """
        Return true if the project already has a test group with the specified name.
        """
        assert name is not None, "Name must not be None"
        assert len(name) > 0, "Name must not be empty string"
        return name in self.test_groups

    def create_test_group(self, name: str) -> TestGroup:
        """
        Return a test group with the specified name.  Add the test group to the dictionary of
        test groups,

        Arguments:
            name - the name of the new test group
        """
        assert not self.has_test_group(name), "There is already a test group with this name: " + name
        test_group = TestGroup(self)
        test_group.test_group_name = name
        self.test_groups[name] = test_group
        return test_group

    def fetch_test_group(self, name: str) -> TestGroup:
        """
        Return a test group with the specified name.  The project must contain this test group.

        Arguments:
            name - the name of a test group
        """
        assert name is not None, "Name must not be None"
        assert self.has_test_group(name), "Project does not have a test group with name: " + name
        return self.test_groups[name]

    def has_environment(self, name: str) -> bool:
        """
        Return true if the project has an environment with the specified name.
        """
        assert name is not None, "Name must not be None"
        assert len(name) > 0, "Name must not be empty string"
        return name in self.environments

    def create_environment(self, name: str) -> Environment:
        """
        Return a new environment with the specified name.

        Arguments:
            name - the name of the environment
        """
        assert not self.has_environment(name), "This environment already exists: " + name
        environment = Environment(self)
        environment.env_name = name
        self.environments[name] = environment
        return environment

    def fetch_environment(self, name) -> Environment:
        """
        Return the environment with the specified name.  There must be an environment with that name.

        Arguments:
            name - the name of the environment
        """
        assert self.has_environment(name), "Project does not have a test group with name: " + name
        return self.environments[name]

    def has_application_type(self, name: str) -> bool:
        """
        Return True if this project has an application type with the specified name.

        Arguments:
            name - the name of the application type
        """
        assert name is not None, "Name must not be None"
        assert len(name) > 0, "Name must not be empty string"
        return name in self.application_types

    def create_application_type(self, name: str) -> ApplicationType:
        """
        Return a new application type.

        Arguments:
            name - name of the application type
        """
        assert not self.has_application_type(name), "Application type already exists: " + name
        application_type = ApplicationType(self)
        application_type.application_type_name = name
        self.application_types[name] = application_type
        return application_type

    def fetch_application_type(self, name: str) -> ApplicationType:
        """
        Return an existing application type with the specified name.

        Arguments:
            name - the name of the application type
        """
        assert self.has_application_type(name), "Project does not have an application type with this name:  " + name
        return self.application_types[name]
