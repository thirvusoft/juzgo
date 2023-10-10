import frappe
from frappe import _
from frappe.utils.nestedset import get_descendants_of


@frappe.whitelist()
def get_bank_cash_jh(company=None,account=None,to_date=None):
    if not account:
        account = "Cash - JH"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }
@frappe.whitelist()
def axis_od_jh_balance(company=None,account=None,to_date=None):
    if not account:
        account = "AXIS OD - JH"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

@frappe.whitelist()
def axis_jh_balance(company=None,account=None,to_date=None):
    if not account:
        account = "AXIS - JH"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

@frappe.whitelist()
def icici_jh_balance(company=None,account=None,to_date=None):
    if not account:
        account = "ICICI - JH"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

@frappe.whitelist()
def juzgo_llp_icici_jh_balance(company=None,account=None,to_date=None):
    if not account:
        account = "Juzgo LLP - ICICI - JH"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

@frappe.whitelist()
def juzgo_llp_jh_balance(company=None,account=None,to_date=None):
    if not account:
        account = "Juzgo LLP - JH"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

@frappe.whitelist()
def icici_llp_jhw_balance(company=None,account=None,to_date=None):
    if not account:
        account = "ICICI LLP - JHW"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

@frappe.whitelist()
def cash_jhw_balance(company=None,account=None,to_date=None):
    if not account:
        account = "Cash - JHW"
    gl_entries = get_gl_entries(account, to_date)
    result = build_result(account, gl_entries)

    return {
        "value": result,
        "fieldtype": "Currency",
    }

def build_result(account, gl_entries):
    result = 0
    # get balances in debit
    for entry in gl_entries:
        result += entry.debit - entry.credit
        
    return result


def get_gl_entries(account, to_date):
    child_accounts = get_descendants_of("Account", account, ignore_permissions=True)
    child_accounts.append(account)

    return frappe.db.get_all(
        "GL Entry",
        fields=["posting_date", "debit", "credit"],
        filters=[
            dict(posting_date=("<", to_date)),
            dict(account=("in", child_accounts)),
            dict(voucher_type=("!=", "Period Closing Voucher")),
        ],
        order_by="posting_date asc",
    )
