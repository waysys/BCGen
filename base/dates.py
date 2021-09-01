# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------

__author__ = 'Bill Shaffer'
__version__ = "2021-09-01"

"""
This module performs certain dte calculations.
"""

import sys
from base.testexception import TestException
from datetime import timedelta, datetime, date

days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def prior_day(dte):
    """
    Compute the date of the day before the argument.

    Argument:
        dte - a date
    """
    return dte - timedelta(days=1)


def next_day(dte):
    """
    Compute the date of the day after the argument.

    Argument:
        dte - a date
    """
    return dte + timedelta(days=1)


def prior_month(dte):
    """
    Compute the datetime of the first day of the prior month.

    Argument:
        dte - a date
    """
    year = dte.year
    month = dte.month
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    return datetime(year, month, 1)


def next_month(dte):
    """
    Return a date that is the first of the month after the current dte.

    Argument:
        dte - the date being used to compute the next month
    """
    month = dte.month
    year = dte.year
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    return datetime(year, month, 1)


def prior_midnight(dte):
    """
    Return a datetime one second before the start of the day indicated by date.
    For example, if the date is 2019-03-01 00:00:00, this function returns 2019-02-28 23:59:59.
    """
    return dte - timedelta(seconds=1)


def beginning_of_month(dte):
    """
    Return the first day of the month where the year and month equal the corresponding year and month
    in dte parameters.

    Argument:
        dte - the date of interest
    """
    year = dte.year
    month = dte.month
    first = datetime(year, month, 1)
    return first


def first_of_year(dte):
    """
    Return the first day of the year for the specified date.

    Argument:
        dte - a date
    """
    year = dte.year
    first = datetime(year, 1, 1)
    return first


def month_year(dte):
    """
    Return a string in the format MM-YYYY where MM is the month of the dte and YYYY is the year of the dte.
    If the month is less than 10, MM is a single digit.

    Argument:
        dte - the dte to use in making the string
    """
    result = str(dte.month) + "-" + str(dte.year)
    return result


def month_id(dte):
    """
    Return an integer in the format YYYYMM.

    Argument:
        dte - the dte to use in making the month id.
    """
    result = dte.year * 100 + dte.month
    return result


def next_month_id(monthid):
    """
    Return a month id that is one month ahead of the input.
    
    Argument:
        monthid - a valid month id in the format of YYYYMM
    """
    month = monthid % 100
    year = monthid // 100
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    newid = year * 100 + month
    return newid


def convert_month_id_to_reporting_date(monthid):
    """
    Convert a month id into the associated reporting date.

    Argument:
        monthid - a month id in the form of YYYYMM
    """
    year = monthid // 100
    month = monthid % 100
    dte = datetime(year, month, 1)
    dte = next_month(dte)
    return dte


def date_id(dte):
    """
    Return an integer in the format YYYYMMDD
    """
    result = dte.year * 10000 + dte.month * 100 + dte.day
    return result


def end_of_month(dte):
    """
    Return the date of the last day of the month containing the specified date.

    Argument:
        dte - the date used to determine the end of the month.
    """
    year = dte.year
    month = dte.month
    last_day = days_in_months[month - 1]
    if is_leap_year(year) and (month == 2):
        last_day = 29
    last_day_month = datetime(year, month, last_day)
    return last_day_month


def first_of_next_month(dte):
    """
    Return the dte of the first day of the month after the month containing the specified date,
    except when dte is the first day of the month.  In this case, just use this date.

    Argument:
        dte - the date used to determine the end of the month.
    """
    if dte.day == 1:
        return dte
    year = dte.year
    month = dte.month
    day = 1
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    first_of_month = datetime(year, month, day)
    return first_of_month


def is_leap_year(year):
    """
    Return true if year is a leap year.

    Argument:
        year - the year being tested
    """
    assert year >= 1900, "Year must be greater than 1899 - " + str(year)
    result = False
    if (year % 400) == 0:
        result = True
    elif (year % 100) == 0:
        result = False
    elif (year % 4) == 0:
        result = True
    return result


def safe_date_convert(adate):
    """
    Convert a datetime to a date.  If the date is actually a date, just return it.

    Arguments:
        adate - either a datetime or a date
    """
    if type(adate) == datetime:
        result = adate.date()
    elif type(adate) == date:
        result = adate
    else:
        assert False, "Adate is neither a datetime or date: " + str(type(adate))
    return result


def end_of_last_month(dte):
    """
    Return the last day of the month prior to the specified date.

    Argument:
        dte - the date of the report
    """
    prior_month_day = prior_month(dte)
    last_day_of_month = end_of_month(prior_month_day)
    return last_day_of_month


def convert_to_string(dte):
    """
    Convert the date into a string in the format mm/dd/yyyy

    Argument:
        dte - the date to be converted
    """
    value = dte.strftime("%m-%d-%Y")
    return value


def convert_to_iso_string(dte):
    """
    Convert the string to a format:  YYYY-MM-DD

    Argument:
        dte - the date being converted
    """
    value = dte.strftime("%Y-%m-%d")
    return value


def convert_to_date(value):
    """
    Convert a string in the format mm/dd/yyyy to a date.

    Argument:
        value - the string value to convert
    """
    dte = datetime.strptime(value, "%m-%d-%Y")
    return dte


def convert_to_datetime(dte):
    """
    Convert a date to a datetime.

    Argument:
        dte - a dte
    """
    dt = datetime(dte.year, dte.month, dte.day)
    return dt


def process_reporting_date(args):
    """
    This function handles the capture of the reporting dte from the command line.
    It assumes the date is in the format YYYY-MM-DD.

    Arguments:
        args - the command line argument array
    """
    if len(args) < 2:
        print("Reporting dte was not provided.\n  Usage: python script YYYY-MM-DD")
        sys.exit(1)
    try:
        if args[1].lower() == 'current':
            dte = datetime.now()
            dte = datetime(dte.year, dte.month, dte.day, 0, 0, 0)
        else:
            dte = datetime.strptime(args[1], "%Y-%m-%d")
            dte = next_day(dte)
    except Exception as e:
        print("Invalid dte: " + args[1])
        print(str(e))
        raise TestException(str(e))
    return dte


def process_env_date(env_date):
    """Return the specified dte.  If the input is 'current', return the current dte time.

    Argument:
        env_date - a string obtained from the ENV_DATE environmental variable.  It should
           contain the reporting dte.
    """
    if env_date.lower() == 'current':
        dte = datetime.now()
        dte = datetime(dte.year, dte.month, dte.day, 0, 0, 0)
    else:
        dte = datetime.strptime(env_date, "%Y-%m-%d")
    return dte


def calc_first_of_month(reporting_date):
    """
    Return the first of the month dte based on the reporting date.

    Argument:
        reporting_date - the reporting date
    """
    if reporting_date.day == 1:
        first_of_month = reporting_date
    else:
        first_of_month = next_day(end_of_month(reporting_date))
    return first_of_month


def difference(last_date, first_date):
    """Compute the number of days in the dte range.

    Arguments:
        last_date - the end of the dte range
        first_date - the beginning of the dte range
    """
    diff = (last_date - first_date).days
    return diff


def today():
    """
    Return the current date as a string in the format yyyy-mm-dd
    """
    return date.today().strftime("%Y-%m-%d")


def convert_string_to_date(date_string):
    if isinstance(date_string, datetime):
        a_date = date_string
    else:
        try:
            #
            # Need to remove extraneous last digit on the microsecondes
            #
            length = len(date_string) - 1
            date_string = date_string[0: length]
            a_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f")
        except TypeError as err:
            raise TestException("Date string is not right type: " + str(err))
        except ValueError as err:
            raise TestException("Error converting date string " + date_string + ": " + str(err))
    return a_date.date()
