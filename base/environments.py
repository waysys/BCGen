# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "2021-09-01"

"""
This module contains parameters for database connections.  These parameters
can be reused in different tests
"""

import os
import sys

from base.dates import process_env_date

# -------------------------------------------------------------------------------
# Database Definitions
# -------------------------------------------------------------------------------

params = {
    "COMMON01PC": ["COMMON01", "GWPC"],
    "COMMON01CC": ["COMMON01", "GWCC"]
}

# -------------------------------------------------------------------------------
# Functions for obtaining the database environment
# -------------------------------------------------------------------------------


def has_environment(environ):
    """
    Return true if environ is a supported environment.

    Argument:
        environ - a string with the name of the environment.
    """
    return environ in params


def get_environment(environ):
    """
    Return a list of values for the connection to the database.  If the environment
    name is not in the params dictionary, throw an exception.

    Arguments:
        environ - the name of the environment
    """
    result = params[environ]
    return result


def fetch_environment_code(environ_variable, default):
    """
    Return the environment code from the specified environmental variable.

    Arguments:
        environ_variable - the environmental variable that has the code
        default - the default code if the environmental variable does not exist
    """
    assert environ_variable is not None, "Environmental variable must not be None"
    assert default is not None, "Default environment code must not be None"
    env_code = os.getenv(environ_variable, default)
    if environ_variable == 'ENV_REPORT':
        return env_code
    if not has_environment(env_code):
        print("Unknown environment variable: " + env_code)
        sys.exit(1)
    return env_code
