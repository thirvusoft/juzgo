# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate

def execute(filters=None):
	columns, data  = get_columns(filters), get_data(filters)

	return columns, data

def get_data(filters):
	gpe =get_payment_entry(filter)
	return gpe
def get_payment_entry(filter):
	payment_entry = frappe.db.sql(
		"""
			select
				project as project_id, project_name, posting_date, party_type, party, party_name
				doctype, name, remarks
			from `tabPayment Entry`
			
		""",
		as_dict=1,
	)
	return payment_entry
def get_columns(filters):
	columns = [
		{
			"label": _("Project Id"),
			"fieldname": "project_id",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Project Name"),
			"fieldname": "project_name",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 130,
		},
		{"label": _("Voucher Type"), "fieldname": "voucher_type", "fieldtype":"Data", "width": 120},
		{
			"label": _("Voucher No"),
			"fieldname": "voucher_no",
			"fieldtype": "Dynamic Link",
			"options": "voucher_type",
			"width": 180,
		},
		{
			"label": _("Party"),
			"fieldname": "party",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Net Total"),
			"fieldname": "net_total",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _("Tax"),
			"fieldname": "tax",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _("Total Amount"),
			"fieldname": "total_amount",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _("Paid"),
			"fieldname": "paid",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _("Outstanding Amount"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Float",
			"width": 130,
		},
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 130,
		},
		{
			"label": _("Due Days"),
			"fieldname": "due_days",
			"fieldtype": "Data",
			"width": 130,
		},
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Text",
			"width": 130,
		},
	]
	return columns