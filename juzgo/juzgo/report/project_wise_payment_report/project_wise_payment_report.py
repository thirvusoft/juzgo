# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _, _dict
from frappe.utils import cstr, getdate

def execute(filters=None):
	columns, data  = get_columns(filters), get_data(filters)

	return columns, data
def assign_row(row, is_payment=0):
	rows=[]
	totals=[]
	if is_payment == 1:
		for i in ["Supplier","Customer"]:
			rows.append({'project_id':frappe.bold(i+" Payment Entry")})
			total = {'party':frappe.bold("Total"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
			for j in row:
				if i == j.party_type:
					total['net_total'] = total['net_total'] + (j.get('net_total') or 0)
					total['tax'] = total['tax'] + (j.get('tax') or 0)
					total['total_amount'] = total['total_amount'] + (j.total_amount or 0)
					total['paid'] = total['paid'] + (j.get('paid') or 0)
					total['outstanding_amount'] = total['outstanding_amount'] + (j.get('outstanding_amount') or 0)
					rows.append(j)
					total.update({"voucher_no":frappe.bold(i+" "+j.voucher_type)})
			if rows:
				rows.append(total)
				totals.append(total)
	else:
		total = {'party':frappe.bold("Total"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		for j in row:
			total['net_total'] = total['net_total'] + (j.get('net_total') or 0)
			total['tax'] = total['tax'] + (j.get('tax') or 0)
			total['total_amount'] = total['total_amount'] + (j.total_amount or 0)
			total['paid'] = total['paid'] + (j.get('paid') or 0)
			total['outstanding_amount'] = total['outstanding_amount'] + (j.get('outstanding_amount') or 0)
			rows.append(j)
			total.update({"voucher_no":frappe.bold(j.voucher_type)})
		if rows:
			rows.append(total)
			totals.append(total)
	return rows, totals
def get_profit(total):
		profit = {'party':frappe.bold("Profit"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		sp = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		pp = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		dd = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		for tot in total:
			if tot.get('voucher_no') == "<strong>Sales Invoice</strong>":
				sp['net_total'] = (tot.get('net_total') or 0)
				sp['tax'] = (tot.get('tax') or 0)
				sp['total_amount'] = (tot.get('total_amount') or 0)
				sp['paid'] = (tot.get('paid') or 0)
				sp['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
			if tot.get('voucher_no') == '<strong>Purchase Invoice</strong>':
				pp['net_total'] = (tot.get('net_total') or 0)
				pp['tax'] = (tot.get('tax') or 0)
				pp['total_amount'] = (tot.get('total_amount') or 0)
				pp['paid'] = (tot.get('paid') or 0)
				pp['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
			if tot.get('voucher_no') == '<strong>Delivery Note</strong>':
				dd['net_total'] = (tot.get('net_total') or 0)
				dd['tax'] = (tot.get('tax') or 0)
				dd['total_amount'] = (tot.get('total_amount') or 0)
				dd['paid'] = (tot.get('paid') or 0)
				dd['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
		profit['net_total'] = sp['net_total'] - pp['net_total'] - dd['net_total']
		profit['tax'] = sp['tax'] - pp['tax'] - dd['tax']
		profit['total_amount'] = sp['total_amount'] - pp['total_amount'] - dd['total_amount']
		profit['paid'] = sp['paid'] - pp['paid'] - dd['paid']
		profit['outstanding_amount'] = sp['outstanding_amount'] - pp['outstanding_amount'] - dd['outstanding_amount'] 
		return profit
def get_data(filters):
	if filters.get("project"):
		row = []
		total =[]
		gpi = get_purchase_invoice(filters)
		one_row,one_total = assign_row(gpi)
		row = row+ one_row
		total = total+one_total

		gsi = get_sales_invoice(filters)
		one_row,one_total = assign_row(gsi)
		row = row+ one_row
		total = total+one_total

		gdn = get_delivery_note(filters)
		one_row,one_total = assign_row(gdn)
		row = row+ one_row
		total = total+one_total
		total.append(get_profit(total))
		
		gpe = get_payment_entry(filters)
		one_row,one_total = assign_row(gpe,is_payment=1)
		row = row+ one_row
		total = total+one_total
		
		row.append({})
		
		for tot in total:
			row.append(tot)

	else:
		get_project = frappe.get_all("Project",fields=["project_name","name"])
		row = []
		for i in get_project:
			total =[]
			row.append({'project_id':frappe.bold("Project Name :-"),'project_name':frappe.bold(i.project_name)})

			gpi = get_purchase_invoice(filters,i.name)
			one_row,one_total = assign_row(gpi)
			row = row+ one_row
			total = total+one_total

			gsi = get_sales_invoice(filters,i.name)
			one_row,one_total = assign_row(gsi)
			row = row+ one_row
			total = total+one_total
			
			gdn = get_delivery_note(filters,i.name)
			one_row,one_total = assign_row(gdn)
			row = row+ one_row
			total = total+one_total
			total.append(get_profit(total))
			
			gpe = get_payment_entry(filters,i.name)
			one_row,one_total = assign_row(gpe,is_payment=1)
			row = row+ one_row
			total = total+one_total
			
			row.append({})
			for tot in total:
				row.append(tot)
		

	return row
def get_conditions(filters):
	conditions = "docstatus = 1 and "
	if filters.get("project"):
		conditions = conditions+"project = '{0}'".format(filters.get("project"))
	return conditions

def get_payment_entry(filters,project=None):
	conditions =  get_conditions(filters) or ""
	if project:
		conditions = conditions+"project = '{0}'".format(project)
	payment_entry = frappe.db.sql(
		"""
			select
				project as project_id, project_name, posting_date, party_type, party, party_name,
				name as voucher_no, remarks, unallocated_amount as paid	
			from `tabPayment Entry`
			where {conditions}
			
		""".format(conditions = conditions),
		as_dict=1,
	)
	for i in payment_entry:
		i.voucher_type = "Payment Entry"
	return payment_entry

def get_sales_invoice(filters,project=None):
	conditions = get_conditions(filters) or ""
	if project:
		conditions = conditions+"project = '{0}'".format(project)
	sales_invoice = frappe.db.sql(
		"""
			select
				project as project_id, project_name, posting_date, customer as party,
				name as voucher_no, net_total, total_taxes_and_charges as tax, grand_total as total_amount, grand_total - outstanding_amount as paid, outstanding_amount, due_date	
			from `tabSales Invoice`
			where {conditions}
			
		""".format(conditions = conditions),
		as_dict=1,
	)
	for i in sales_invoice:
		i.voucher_type = "Sales Invoice"
	return sales_invoice

def get_purchase_invoice(filters,project=None):
	conditions = get_conditions(filters) or ""
	if project:
		conditions = conditions+"project = '{0}'".format(project)
	purchase_invoice = frappe.db.sql(
		"""
			select
				project as project_id, project_name, posting_date, supplier as party,
				name as voucher_no, net_total, total_taxes_and_charges as tax, grand_total as total_amount, grand_total - outstanding_amount as paid, outstanding_amount, due_date	
			from `tabPurchase Invoice`
			where {conditions}
			
		""".format(conditions = conditions),
		as_dict=1,
	)
	for i in purchase_invoice:
		i.voucher_type = "Purchase Invoice"
	return purchase_invoice

def get_delivery_note(filters,project=None):
	conditions = get_conditions(filters) or ""
	if project:
		conditions = conditions+"project = '{0}'".format(project)
	delivery_note = frappe.db.sql(
		"""
			select
				project as project_id, project_name, posting_date, customer as party,
				name as voucher_no, net_total, total_taxes_and_charges as tax, rounded_total as total_amount
			from `tabDelivery Note`
			where {conditions}
			
		""".format(conditions = conditions),
		as_dict=1,
	)
	for i in delivery_note:
		i.voucher_type = "Delivery Note"
	return delivery_note
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