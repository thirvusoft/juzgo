# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import (
	delete_contact_and_address,
	load_address_and_contact,
)
class HotelDetails(Document):
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
	def on_trash(self):
		delete_contact_and_address("Hotel Details", self.name)
@frappe.whitelist()
def jtt_creation(name,doctype,user):
	if(name and doctype and user):
		if not frappe.db.exists('JTT',{"ref_doctype": doctype, "ref_name": name}):
			new_doc = frappe.get_doc({"doctype": "JTT", "ref_doctype": doctype, "ref_name": name, "created_by": user})
			new_doc.save()
			return new_doc.name
		else:
			get_doc = frappe.get_doc("JTT", {"ref_doctype": doctype, "ref_name": name})
			return get_doc.name
	return 0 