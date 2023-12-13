# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

from datetime import datetime
from frappe.utils import cint, date_diff, flt, getdate
from frappe.utils import today
import frappe
from frappe import _, qb, scrub, _dict
from frappe.utils import cstr, getdate

def execute(filters=None):
	columns, data  = get_columns(filters), get_data(filters)

	return columns, data
def assign_row(row, is_payment=None):
	rows=[]
	totals=[]
	if is_payment and row:
		for i in is_payment:
			rows.append({'voucher_no':frappe.bold(i+" Advance Amount")})
			total = {'party':frappe.bold(i+" Advance Total"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
			account_head = frappe.get_all("Account",{"account_type":['in',['Cash','Bank']],"is_group":0})
			for ah in account_head:
				total[scrub(ah.name)] = 0
			for j in row:
				if i == j.party_type:
					total['net_total'] = total['net_total'] + (j.get('net_total') or 0)
					total['tax'] = total['tax'] + (j.get('tax') or 0)
					total['total_amount'] = total['total_amount'] + (j.total_amount or 0)
					total['paid'] = total['paid'] + (j.get('paid') or 0)
					total['outstanding_amount'] = total['outstanding_amount'] + (j.get('outstanding_amount') or 0)
					if j.party_type == "Supplier":
						j[scrub(j.paid_from)] = (j.get('paid') or 0)
						total[scrub(j.paid_from)] = total[scrub(j.paid_from)] + (j.get('paid') or 0)
					elif j.party_type == "Customer":
						j[scrub(j.paid_to)] = (j.get('paid') or 0)
						total[scrub(j.paid_to)] = total[scrub(j.paid_to)] + (j.get('paid') or 0)
					if j.get('paid'):
						rows.append(j)
					total.update({"party":frappe.bold(i+" Advance Total")})
			if rows:
				rows.append(total)
				totals.append(total)
	else:
		if row:
			rows.append({'voucher_no':frappe.bold(row[0].voucher_type)})
			total = {'party':frappe.bold(row[0].voucher_type+" Total"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
			account_head = frappe.get_all("Account",{"account_type":['in',['Cash','Bank']],"is_group":0})
			for ah in account_head:
				total[scrub(ah.name)] = 0
			for j in row:
				if j.get('voucher_no'):
					for ah in account_head:
						j[scrub(ah.name)] = 0
					account_head_name = frappe.get_all("Payment Entry Reference",filters={"reference_name":j.get('voucher_no')},fields=["parent","allocated_amount"])
					for set_amt_acc in account_head_name:
						p_entry = frappe.get_doc("Payment Entry",set_amt_acc.parent)
						if p_entry.payment_type == "Receive":
							j[scrub(p_entry.paid_to)] = j[scrub(p_entry.paid_to)] + (set_amt_acc.get('allocated_amount') or 0)
							total[scrub(p_entry.paid_to)] = total[scrub(p_entry.paid_to)] + (set_amt_acc.get('allocated_amount') or 0)
						elif p_entry.payment_type == "Pay":
							j[scrub(p_entry.paid_from)] = j[scrub(p_entry.paid_from)] +(set_amt_acc.get('allocated_amount') or 0)
							total[scrub(p_entry.paid_from)] = total[scrub(p_entry.paid_from)] + (set_amt_acc.get('allocated_amount') or 0)
				total['net_total'] = total['net_total'] + (j.get('net_total') or 0)
				total['tax'] = total['tax'] + (j.get('tax') or 0)
				total['total_amount'] = total['total_amount'] + (j.total_amount or 0)
				total['paid'] = total['paid'] + (j.get('paid') or 0)
				total['outstanding_amount'] = total['outstanding_amount'] + (j.get('outstanding_amount') or 0)
				rows.append(j)
				total.update({"party":frappe.bold(j.voucher_type+" Total")})
			if rows:
				rows.append(total)
				totals.append(total)
	return rows, totals
def get_diff(total):
		diff = {'party':frappe.bold("Diff"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		sp = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		pp = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		dd = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		account_head = frappe.get_all("Account",{"account_type":['in',['Cash','Bank']],"is_group":0})
		for ah in account_head:
			diff[scrub(ah.name)] = 0
			sp[scrub(ah.name)] = 0
			pp[scrub(ah.name)] = 0
			dd[scrub(ah.name)] = 0
		for tot in total:
			if tot.get('party') == "<strong>Sales Invoice Total</strong>":
				sp['net_total'] = (tot.get('net_total') or 0)
				sp['tax'] = (tot.get('tax') or 0)
				sp['total_amount'] = (tot.get('total_amount') or 0)
				sp['paid'] = (tot.get('paid') or 0)
				sp['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					sp[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
			if tot.get('party') == '<strong>Purchase Invoice Total</strong>':
				pp['net_total'] = (tot.get('net_total') or 0)
				pp['tax'] = (tot.get('tax') or 0)
				pp['total_amount'] = (tot.get('total_amount') or 0)
				pp['paid'] = (tot.get('paid') or 0)
				pp['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					pp[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
			if tot.get('party') == '<strong>Delivery Note Total</strong>':
				dd['net_total'] = (tot.get('net_total') or 0)
				dd['tax'] = (tot.get('tax') or 0)
				dd['total_amount'] = (tot.get('total_amount') or 0)
				dd['paid'] = (tot.get('paid') or 0)
				dd['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					dd[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
		diff['net_total'] = sp['net_total'] - pp['net_total'] - dd['net_total']
		diff['tax'] = sp['tax'] - pp['tax'] - dd['tax']
		diff['total_amount'] = sp['total_amount'] - pp['total_amount'] - dd['total_amount']
		diff['paid'] = sp['paid'] - pp['paid'] - dd['paid']
		diff['outstanding_amount'] = sp['outstanding_amount'] - pp['outstanding_amount'] - dd['outstanding_amount'] 
		for ah in account_head:
			diff[scrub(ah.name)] = sp[scrub(ah.name)] - pp[scrub(ah.name)] - dd[scrub(ah.name)] 
		return diff

def get_net_in_hand(total):
		net_in_hand = {'party':frappe.bold("Net in Hand"),'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		sp = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		pp = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		dd = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		ad_pay = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		ad_re = {'net_total':0, 'tax':0,'total_amount':0,'paid':0,'outstanding_amount':0}
		account_head = frappe.get_all("Account",{"account_type":['in',['Cash','Bank']],"is_group":0})
		for ah in account_head:
			net_in_hand[scrub(ah.name)] = 0
			sp[scrub(ah.name)] = 0
			pp[scrub(ah.name)] = 0
			dd[scrub(ah.name)] = 0
			ad_pay[scrub(ah.name)] = 0
			ad_re[scrub(ah.name)] = 0
		for tot in total:
			if tot.get('party') == "<strong>Sales Invoice Total</strong>":
				sp['net_total'] = (tot.get('net_total') or 0)
				sp['tax'] = (tot.get('tax') or 0)
				sp['total_amount'] = (tot.get('total_amount') or 0)
				sp['paid'] = (tot.get('paid') or 0)
				sp['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					sp[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
			if tot.get('party') == '<strong>Purchase Invoice Total</strong>':
				pp['net_total'] = (tot.get('net_total') or 0)
				pp['tax'] = (tot.get('tax') or 0)
				pp['total_amount'] = (tot.get('total_amount') or 0)
				pp['paid'] = (tot.get('paid') or 0)
				pp['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					pp[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
			if tot.get('party') == '<strong>Delivery Note Total</strong>':
				dd['net_total'] = (tot.get('net_total') or 0)
				dd['tax'] = (tot.get('tax') or 0)
				dd['total_amount'] = (tot.get('total_amount') or 0)
				dd['paid'] = (tot.get('paid') or 0)
				dd['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					dd[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
			if tot.get('party') == '<strong>Supplier Advance Total</strong>':
				ad_pay['net_total'] = (tot.get('net_total') or 0)
				ad_pay['tax'] = (tot.get('tax') or 0)
				ad_pay['total_amount'] = (tot.get('total_amount') or 0)
				ad_pay['paid'] = (tot.get('paid') or 0)
				ad_pay['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					ad_pay[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
			if tot.get('party') == '<strong>Customer Advance Total</strong>':
				ad_re['net_total'] = (tot.get('net_total') or 0)
				ad_re['tax'] = (tot.get('tax') or 0)
				ad_re['total_amount'] = (tot.get('total_amount') or 0)
				ad_re['paid'] = (tot.get('paid') or 0)
				ad_re['outstanding_amount'] = (tot.get('outstanding_amount') or 0)
				for ah in account_head:
					ad_re[scrub(ah.name)] = (tot.get(scrub(ah.name)) or 0)
		net_in_hand['net_total'] = sp['net_total'] - pp['net_total'] - dd['net_total'] + (ad_re['net_total'] - ad_pay['net_total'])
		net_in_hand['tax'] = sp['tax'] - pp['tax'] - dd['tax'] + (ad_re['tax'] - ad_pay['tax'])
		net_in_hand['total_amount'] = sp['total_amount'] - pp['total_amount'] - dd['total_amount'] + (ad_re['total_amount'] - ad_pay['total_amount'])
		net_in_hand['paid'] = sp['paid'] - pp['paid'] - dd['paid'] + (ad_re['paid'] - ad_pay['paid'])
		net_in_hand['outstanding_amount'] = sp['outstanding_amount'] - pp['outstanding_amount'] - dd['outstanding_amount']  + (ad_re['outstanding_amount'] - ad_pay['outstanding_amount'])
		for ah in account_head:
			net_in_hand[scrub(ah.name)] = sp[scrub(ah.name)] - pp[scrub(ah.name)] - dd[scrub(ah.name)] + (ad_re[scrub(ah.name)] - ad_pay[scrub(ah.name)])
		return net_in_hand
def get_data(filters):
	row = []
	if filters.get("project") and filters.get("group_by") == "Group by Voucher":
		row = []
		total =[]
		if filters.get("purchase_invoice"):
			gpi = get_purchase_invoice(filters)
			one_row,one_total = assign_row(gpi)
			row = row+ one_row
			total = total+one_total
		if filters.get("sales_invoice"):
			gsi = get_sales_invoice(filters)
			one_row,one_total = assign_row(gsi)
			row = row+ one_row
			total = total+one_total
		if filters.get("delivery_note"):
			gdn = get_delivery_note(filters)
			one_row,one_total = assign_row(gdn)
			row = row+ one_row
			total = total+one_total
		if total:
			total.append(get_diff(total))
		
		is_payment = []
		if filters.get("purchase_payment_entry"):
			is_payment.append("Supplier")
		if filters.get("sales_payment_entry"):
			is_payment.append("Customer")
		if filters.get("sales_payment_entry") or filters.get("purchase_payment_entry"):
			gpe = get_payment_entry(filters)
			one_row,one_total = assign_row(gpe,is_payment)
			row = row+ one_row
			total = total+one_total
		if total:
			total.append(get_net_in_hand(total))

		row.append({})
		
		for tot in total:
			row.append(tot)

	elif not filters.get("project")  and filters.get("group_by") == "Group by Voucher":
		get_project = frappe.get_all("Project",fields=["project_name","name"])
		row = []
		for i in get_project:
			rowss=[]
			total =[]

			if filters.get("purchase_invoice"):
				gpi = get_purchase_invoice(filters,i.name)
				one_row,one_total = assign_row(gpi)
				rowss = rowss+ one_row
				total = total+one_total

			if filters.get("sales_invoice"):
				gsi = get_sales_invoice(filters,i.name)
				one_row,one_total = assign_row(gsi)
				rowss = rowss+ one_row
				total = total+one_total

			if filters.get("delivery_note"):
				gdn = get_delivery_note(filters,i.name)
				one_row,one_total = assign_row(gdn)
				rowss = rowss+ one_row
				total = total+one_total
			if total:
				total.append(get_diff(total))

			is_payment = []
			if filters.get("purchase_payment_entry"):
				is_payment.append("Supplier")
			if filters.get("sales_payment_entry"):
				is_payment.append("Customer")
			if filters.get("sales_payment_entry") or filters.get("purchase_payment_entry"):
				gpe = get_payment_entry(filters,i.name)
				one_row,one_total = assign_row(gpe,is_payment)
				rowss = rowss+ one_row
				total = total+one_total
			if total:
				total.append(get_net_in_hand(total))

			for tot in total:
				rowss.append(tot)
				
			if rowss:
				row.append({'project_id':frappe.bold("Project Name :-"),'project_name':frappe.bold(i.project_name)})
				row = row+ rowss
			
	elif filters.get("project") and (filters.get("group_by") == "Group by Voucher (Consolidated)"):
		row = []
		total =[]
		if filters.get("purchase_invoice"):
			gpi = get_purchase_invoice(filters)
			one_row,one_total = assign_row(gpi)
			total = total+one_total
		if filters.get("sales_invoice"):
			gsi = get_sales_invoice(filters)
			one_row,one_total = assign_row(gsi)
			total = total+one_total
		if filters.get("delivery_note"):
			gdn = get_delivery_note(filters)
			one_row,one_total = assign_row(gdn)
			total = total+one_total
		if total:
			total.append(get_diff(total))

		is_payment = []
		if filters.get("purchase_payment_entry"):
			is_payment.append("Supplier")
		if filters.get("sales_payment_entry"):
			is_payment.append("Customer")
		if filters.get("sales_payment_entry") or filters.get("purchase_payment_entry"):
			gpe = get_payment_entry(filters)
			one_row,one_total = assign_row(gpe,is_payment)
			total = total+one_total
		if total:
			total.append(get_net_in_hand(total))
		if total:
			row.append({})
			row.append({'project_id':frappe.bold("Project Name :-"),'project_name':frappe.bold(filters.get("project"))})
		for tot in total:
			row.append(tot)

	elif (filters.get("group_by") == "Group by Voucher (Consolidated)") and not filters.get("project"):
		get_project = frappe.get_all("Project",fields=["project_name","name"])
		row = []
		for i in get_project:
			total =[]

			if filters.get("purchase_invoice"):
				gpi = get_purchase_invoice(filters,i.name)
				one_row,one_total = assign_row(gpi)
				total = total+one_total

			if filters.get("sales_invoice"):
				gsi = get_sales_invoice(filters,i.name)
				one_row,one_total = assign_row(gsi)
				total = total+one_total

			if filters.get("delivery_note"):
				gdn = get_delivery_note(filters,i.name)
				one_row,one_total = assign_row(gdn)
				total = total+one_total
			if total:
				total.append(get_diff(total))

			is_payment = []
			if filters.get("purchase_payment_entry"):
				is_payment.append("Supplier")
			if filters.get("sales_payment_entry"):
				is_payment.append("Customer")
			if filters.get("sales_payment_entry") or filters.get("purchase_payment_entry"):
				gpe = get_payment_entry(filters,i.name)
				one_row,one_total = assign_row(gpe,is_payment)
				total = total+one_total
			if total:
				total.append(get_net_in_hand(total))

			if total:
				row.append({})
				row.append({'project_id':frappe.bold("Project Name :-"),'project_name':frappe.bold(i.project_name)})
			for tot in total:
				row.append(tot)	

	return row
def get_conditions(filters):
	conditions = "docstatus = 1 and company = '{0}' and ".format(filters.get('company'))
	if filters.get("branch"):
		conditions = conditions+"branch = '{0}' and ".format(filters.get("branch"))

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
				name as voucher_no, remarks, unallocated_amount as paid, paid_to, paid_from
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
				project as project_id, project_name, posting_date, customer as party, remarks,
				name as voucher_no, net_total, total_taxes_and_charges as tax, grand_total as total_amount, grand_total - outstanding_amount as paid, outstanding_amount, due_date	
			from `tabSales Invoice`
			where {conditions}
			
		""".format(conditions = conditions),
		as_dict=1,
	)
	for i in sales_invoice:
		i.voucher_type = "Sales Invoice"
		due_days = date_diff(i.due_date, datetime.strptime(today(), '%Y-%m-%d').date())
		if due_days <= 0 and i.outstanding_amount:
			i.due_days = abs(due_days)
	return sales_invoice

def get_purchase_invoice(filters,project=None):
	conditions = get_conditions(filters) or ""
	if project:
		conditions = conditions+"project = '{0}'".format(project)
	purchase_invoice = frappe.db.sql(
		"""
			select
				project as project_id, project_name, posting_date, supplier as party, remarks,
				name as voucher_no, net_total, total_taxes_and_charges as tax, grand_total as total_amount, grand_total - outstanding_amount as paid, outstanding_amount, due_date	
			from `tabPurchase Invoice`
			where {conditions}
			
		""".format(conditions = conditions),
		as_dict=1,
	)
	for i in purchase_invoice:
		i.voucher_type = "Purchase Invoice"
		due_days = date_diff(i.due_date, datetime.strptime(today(), '%Y-%m-%d').date())
		if due_days <= 0 and i.outstanding_amount:
			i.due_days = abs(due_days)
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
			"width": 200,
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
		}]
	account_head = frappe.get_all("Account",{"account_type":['in',['Cash','Bank']],"is_group":0})
	for i in account_head:
		columns.append(
			{
				"label":_(i.name),
				"fieldtype": scrub(i.name),
				"fieldtype": "Float",
				"width": 130,
			}
		)
	columns.append(
		{
			"label": _("Outstanding Amount"),
			"fieldname": "outstanding_amount",
			"fieldtype": "Float",
			"width": 130,
		})
	columns.append(
		{
			"label": _("Due Date"),
			"fieldname": "due_date",
			"fieldtype": "Date",
			"width": 130,
		})
	columns.append(
		{
			"label": _("Due Days"),
			"fieldname": "due_days",
			"fieldtype": "Data",
			"width": 130,
		})
	columns.append(
		{
			"label": _("Remarks"),
			"fieldname": "remarks",
			"fieldtype": "Text",
			"width": 130,
		})
	
	return columns