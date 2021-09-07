# -------------------------------------------------------------------------------
#
#  Copyright (c) 2021 Waysys LLC
#
# -------------------------------------------------------------------------------
# -------------------------------------------------------------------------------
#
__author__ = 'Bill Shaffer'
__version__ = "03-Sep-2021"

"""
This module contains queries of PolicyCenter
"""

from datetime import datetime

from base.connector import Connector
from base.query import Query
from pyodbc import Connection

account_query = """
DECLARE @SelectionStart DATE = ?
DECLARE @SelectionEnd DATE = ?

SELECT [accountnumber] AS AccountNumber,
       cnt.firstname   AS FirstName,
       cnt.lastname    AS LastName,
       cnt.NAME        AS CompanyName,
       ct.typecode     AS ContactType,
       aot.typecode    AS AccountOrgType,
       ast.typecode    AS AccountStatus,
       ic.code         AS IndustryCode,
       acrt.typecode   AS Role,
       acct.createtime AS CreateDate
FROM   [pc_account] acct
       JOIN pc_accountcontact ac
         ON ac.account = acct.id
       JOIN pc_accountcontactrole acr
         ON acr.accountcontact = ac.id
       JOIN pc_contact cnt
         ON ac.contact = cnt.id
       LEFT JOIN pc_industrycode ic
              ON acct.industrycodeid = ic.id
       JOIN pctl_accountorgtype aot
         ON acct.accountorgtype = aot.id
       JOIN pctl_accountcontactrole acrt
         ON acr.subtype = acrt.id
       JOIN pctl_contact ct
         ON cnt.subtype = ct.id
       JOIN pctl_accountstatus ast
         ON acct.accountstatus = ast.id
WHERE  acct.retired = 0
       AND acrt.typecode = 'AccountHolder'
       AND acct.createtime >= @SelectionStart
       AND acct.createtime < @SelectionEnd 
"""


# -------------------------------------------------------------------------------
#  PolicyCenter Queries
# -------------------------------------------------------------------------------


class PolicyCenterQueries:
    """
    This class contains queries of PolicyCenter.
    """

    # ---------------------------------------------------------------------------
    #  Constructor
    # ---------------------------------------------------------------------------

    def __init__(self, cnx: Connection):
        """
        Initialize the instance of a class.

        Argument:
            cnx - a connection to a database
        """
        assert cnx is not None, "Connection for query must not be null"
        self._cnx = cnx
        self.query = Query(self._cnx)
        return

    # ---------------------------------------------------------------------------
    #  Queries
    # ---------------------------------------------------------------------------

    def query_accounts(self, selection_start: datetime, selection_end: datetime) -> list:
        """
        Return a selection of accounts created on or after the selection start and before the
        selection end.

        Arguments:
            selection_start - the earliest date when the accounts were created
            selection_end - the date before which the accounts must have been created
        """
        assert selection_start is not None, "selection start must not be None"
        assert selection_end is not None, "selection end must not be None"
        assert selection_start < selection_end, "selection start " + str(selection_start) + \
                                                " must be before selection end " + str(selection_end)
        results = self.query.query(account_query, selection_start, selection_end)
        return list(results)
