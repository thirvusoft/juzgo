# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Destination(Document):
	pass
@frappe.whitelist()
def connection(name):
	return len(frappe.get_all("Spots",{"destination":name,"is_jtt":1})),len(frappe.get_all("Hotel Details",{"destination":name,"is_jtt":1})),len(frappe.get_all("Restaurant",{"destination":name,"is_jtt":1}))