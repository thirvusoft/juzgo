# -*- coding: utf-8 -*-
# Copyright (c) 2020, Youssef Restom and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import json
import frappe
from frappe.utils import nowdate, flt, cstr
from frappe import _


@frappe.whitelist()
def get_doc_names(doctype):
    return frappe.get_all(doctype,pluck="name")

@frappe.whitelist()
def get_customer_names():
    customers = frappe.db.sql(
        """
        SELECT name, mobile_no, email_id, tax_id, customer_name, primary_address
        FROM `tabCustomer`
        
        ORDER by name
        """,
        as_dict=1,
    )
    return customers

@frappe.whitelist()
def get_project_names():
    project = frappe.db.sql(
        """
        SELECT name, project_name, abbr, phone_number, lead, ca_form
        FROM `tabProject`
        
        ORDER by name
        """,
        as_dict=1,
    )
    return project

@frappe.whitelist()
def get_detailing_names(project=None):

    condition = ''
    if project:
        condition = f'Where project = "{project}"'
    detailing = frappe.db.sql(
        """
        SELECT name, project_name, project, ca_form
        FROM `tabDetailing Page`
        {0}
        ORDER by name
        """.format(condition),
        as_dict=1,
    )
    return detailing

@frappe.whitelist()
def get_detailing(detailing_id):
    detailing = frappe.get_doc("Detailing Page",detailing_id)
    return detailing
@frappe.whitelist()
def get_quotation_compare(quotation_compare_id):
    quotation_compare = frappe.get_doc("DP-Quotation comparission",quotation_compare_id)
    return quotation_compare
@frappe.whitelist()
def get_last_data():
    detailing = frappe.get_all("Detailing Page", filters={"modified_by":frappe.session.user}, fields=["name","modified"], limit=1, order_by="modified desc")
    if not detailing:
        frappe.throw("There is no Detailing Page for recent open, so open from the project.")
    detailing = frappe.get_doc("Detailing Page", detailing[0].name)
    return detailing

@frappe.whitelist()
def save_detailing(detailing_id, detailing_detail):
    data = json.loads(detailing_detail)
    if data.get("name"):
        detailing = frappe.get_doc("Detailing Page", data.get("name"))
        detailing.update(data)
        detailing.save()
        return 1

    return 0


@frappe.whitelist()
def get_caform_names():
    caforms = frappe.db.sql(
        """
        SELECT name, party_name, whatsapp_number, e_mail, company,  quality_of_lead 
        FROM `tabCA Form`
        
        ORDER by name
        """,
        as_dict=1,
    )
    return caforms

@frappe.whitelist()
def get_attach(detailing_detail):
    doc = json.loads(detailing_detail)
    file =[]
    for i in doc.get("common_features"):
        file.append(frappe.get_doc("File",{"file_url":i["airticket"]}))
    return file

@frappe.whitelist()
def get_mailing_details(detailing_detail,item):
    doc = json.loads(detailing_detail)
    item = json.loads(item)
    list={}
    list.update(item)
    if item.get("hotels"):
        list.update({"hotels":doc.get("hotels")})
    if item.get("spots"):
        list.update({"spots":doc.get("spots")})
    if item.get("vehicle"):
        list.update({"vehicle":doc.get("vehicle")})
    if item.get("optional_costs"):
        list.update({"optional_costs":doc.get("optional_cost_needed_for")})
    if item.get("others"):
        list.update({"others":doc.get("others")})
    if item.get("cruise"):
        list.update({"cruise":doc.get("cruise")})
    list.update({"doc":doc})

    return list
@frappe.whitelist()
def get_visa_mailing_details(detailing_detail,item):
    doc = json.loads(detailing_detail)
    item = json.loads(item)
    list={}
    list.update(item)
    list.update({"doc":doc})

    return list   

@frappe.whitelist()
def save_detailing_compare(quotation_comparission_id,quotation_comparission_data):
    data = json.loads(quotation_comparission_data)
    if data.get("name"):
        detailing = frappe.get_doc("DP-Quotation comparission", data.get("name"))
        detailing.update(data)
        detailing.save()
        return 1

    return 0