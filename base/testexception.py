# -------------------------------------------------------------------------------
#
#  Copyright (c) 2019 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "1.00"

"""
This module contains a class for a testing exception.  This exception is thrown
from the testing framework.
"""

# -------------------------------------------------------------------------------
#  Test Exception
# -------------------------------------------------------------------------------


class TestException(Exception):
    """
    This exception identifies the error as arising in the testing framework
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, message):
        """
        Initialize the exception

        Argument:
            message - the error message for the exception
        """
        super().__init__(self, message)
        self._message = message
        return

    @property
    def message(self):
        return self._message

    def __str__(self):
        """
        Return the message associated with this string.
        """
        return self.message
