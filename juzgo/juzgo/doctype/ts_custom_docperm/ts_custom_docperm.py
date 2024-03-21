# Copyright (c) 2024, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class TSCustomDocPerm(Document):
	pass

def after_migrate():

    print("Restoring Role Permissions By Thirvusoft...")

    frappe.db.sql(""" DELETE FROM `tabCustom DocPerm` """)

    permissions = frappe.get_all("TS Custom DocPerm")

    for permission in permissions:

        role_per = frappe.get_doc("TS Custom DocPerm", permission)

        per = frappe.new_doc("Custom DocPerm")

        role_per = role_per.as_dict()

        del role_per['doctype']
        del role_per['name']

        per.update(role_per)

        per.parent = role_per.ts_parent

        per.save(ignore_permissions = True)

        frappe.db.commit()

def before_migrate():

    print("Taking Role Permissions Backup By Thirvusoft...")

    frappe.db.sql(""" DELETE FROM `tabTS Custom DocPerm` """)

    permissions = frappe.get_all("Custom DocPerm")
    
    for permission in permissions:

        role_per = frappe.get_doc("Custom DocPerm", permission)

        per = frappe.new_doc("TS Custom DocPerm")

        role_per = role_per.as_dict()

        del role_per['doctype']
        del role_per['name']

        per.update(role_per)

        per.ts_parent = role_per.parent

        per.save(ignore_permissions = True)

        frappe.db.commit()