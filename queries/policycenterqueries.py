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

from pyodbc import Connection

from base.query import Query

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
       AND ast.typecode = 'Active'
"""


policy_periods_query = """
DECLARE @SelectionEnd DATE = ?
DECLARE @NumberRows INT = ?

SELECT TOP (@NumberRows) ac.accountnumber    AS AccountNumber,
                         pp.policynumber     AS PolicyNumber,
                         pp.periodstart      AS PeriodStart,
                         pp.periodend        AS PeriodEnd,
                         pp.cancellationdate AS CancellationDate,
                         pp.taxsurchargesrpt AS Taxes,
                         pp.totalpremiumrpt  AS Premium,
                         pp.totalcostrpt     AS TotalInvoicedAmount,
                         ps.NAME             AS PaymentPlan,
                         bp.typecode         AS BillingPeriodicity,
                         pps.typecode        AS Status,
                         ps.billingid        AS BillingID
FROM   pc_policyperiod pp
       JOIN pc_policy pl
         ON pp.policyid = pl.id
       JOIN pc_account ac
         ON pl.accountid = ac.id
       JOIN pc_paymentplansummary ps
         ON ps.policyperiod = pp.id
       JOIN pctl_billingperiodicity bp
         ON ps.invoicefrequency = bp.id
       JOIN pctl_policyperiodstatus pps
         ON pp.status = pps.id
WHERE  pp.retired = 0
       AND ps.retired = 0
       AND pp.createtime < @SelectionEnd
       AND pps.typecode = 'Bound'
       AND pp.cancellationdate IS NULL
ORDER  BY pp.createtime DESC 
"""

producer_code_query = """
SELECT org.NAME         AS ProducerName,
       code             AS ProducerCode,
       prs.typecode     AS ProducerStatus,
       adr.addressline1 AS AddressLine1,
       adr.city         AS City,
       st.typecode      AS State,
       adr.postalcode   AS PostalCode
FROM   pc_producercode prc
       JOIN pc_organization org
         ON prc.organizationid = org.id
       JOIN pctl_producerstatus prs
         ON prc.producerstatus = prs.id
       JOIN pc_address adr
         ON prc.addressid = adr.id
       JOIN pctl_state st
         ON adr.state = st.id
WHERE  prc.retired = 0
       AND prs.typecode = 'Active' 
"""

payment_plan_query = """
DECLARE @CurrentID VARCHAR(20) = ?

SELECT DISTINCT pps.billingid AS BillingID,
                pps.NAME      AS PlanName
FROM   pc_paymentplansummary pps
       JOIN pctl_paymentmethod pt
         ON pps.paymentplantype = pt.id
WHERE  pt.typecode = 'Installments'
       AND billingid <> @CurrentID 
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

    def query_policy_periods(self, selection_end: datetime, number_rows: int) -> list:
        """
        Return a list of policy periods created before the selection end date.  The list
        is limited to the number indicated by number_rows.

        The most recently created policy periods are listed first, so this query will return
        the most recently created policy periods created prior to the selection_end date.

        The policy periods will be bound and will not include cancelled policy periods.
        """
        assert selection_end is not None, "selection end must not be None"
        assert number_rows > 0, "The number of rows must be greater than 0, not " + str(number_rows)
        results = self.query.query(policy_periods_query, selection_end, number_rows)
        return list(results)

    def query_producer_code(self):
        """
        Return a list of policy codes with producers.
        """
        results = self.query.query(producer_code_query)
        return list(results)

    def query_payment_plan(self, current_id: str):
        """
        Return a list of installment payment plans, excluding the current plan.

        Arguments:
            current_id - the BillingID of the current payment plan
        """
        results = self.query.query(payment_plan_query, current_id)
        return list(results)
