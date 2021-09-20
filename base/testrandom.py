# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "16-Sep-2021"

"""
This module provides a class for generating a psuedo-random number or a random selection.
"""

from random import randrange, seed

DEFAULT_SEED = 67889


# -------------------------------------------------------------------------------
#  Random
# -------------------------------------------------------------------------------


class Random:
    """
    Perform certain random activities.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, sd: int):
        """
        Initial the instance of this calss

        Arguments:
            sd - the seed to apply to the random number generator.
        """
        seed(sd)
        return

    @staticmethod
    def get_random(number_range: tuple[int, int]) -> str:
        """
        Return a random integer in the specified range as a string.

        Arguments:
            number_range - a pair of integers with the beginning of a range (inclusive) and an
               end of a range (exclusive)
        """
        assert number_range is not None, "Number range must not be None"
        assert len(number_range) == 2, "Number range must have 2 values, not " + str(len(number_range))
        assert number_range[0] < number_range[1], "For number range, first element must be less than second"
        value = randrange(number_range[0], number_range[1])
        return str(value)

    @staticmethod
    def select(weight: int) -> bool:
        """
        Return True if a random number is less than the weight.

        Arguments:
            weight - a value between 0 and 100 inclusive
        """
        random_num = randrange(0, 100)
        return random_num < weight

    @staticmethod
    def select_from_list(a_list: list[str]) -> str:
        """
        Select one of the items in the list at random.

        Arguments:
            a_list - a list of strings
        """
        assert a_list is not None, "The list must not be None"
        assert len(a_list) > 0, "The list must not be empty"
        size = len(a_list)
        random_number = randrange(0, size)
        return a_list[random_number]
