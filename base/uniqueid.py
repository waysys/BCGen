# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "15-Sep-2021"

"""
This module produces strings that are unique over time
"""

import time
import string

MAX_CHARACTERS = 6
DIGITS = string.digits + string.ascii_lowercase


def gen_unique_id() -> str:
    """
    Return a string with MAX_CHARACTERS characters that is unique from any prior strings returned.
    """
    time.sleep(2)
    # number of seconds since the epoch as an integer
    seconds = round(time.time())
    value = int_to_str(seconds, 32)
    value = value[-MAX_CHARACTERS:]
    return value


def int_to_str(original_value: int, base: int) -> str:
    """
    Convert a positive number to a string in a format for the specified base.

    Arguments:
        original_value - the integer to be converted
        base - the base to be used
    """
    #
    # Pre-condition:
    #
    assert original_value > 0, "Value must be greater than zero, not " + str(original_value)
    assert base > 1, "Base must be greater than 1, not " + str(base)
    assert base <= len(DIGITS), "Base is too large for the digits available: " + str(base)
    value = original_value
    digits = ""
    # prior_digits = ""
    # exp = 0
    # Invariant:
    #   value(exp) =
    # 	 if exp == 0 then original_value
    # 	 else value(exp - 1) // base
    #
    #  digit(exp) = value(exp) % base
    #
    #  result(exp) =
    #    if exp ==0 then 0
    #    else (base ** (exp - 1) * (digit(exp - 1)  + result(exp - 1)
    #
    # value(exp) * base ** exp + result(exp) == original_value
    #
    # Bound Function:
    #   t(original_value, exp) = original_value // base ** exp
    while value > 0:
        last_digit = value % base
        digit = DIGITS[last_digit]
        digits += digit
        value = value // base
        # exp = exp + 1
    result = digits[::-1]
    #
    # Post-condition:
    #   result(exp) == original_value
    return result
