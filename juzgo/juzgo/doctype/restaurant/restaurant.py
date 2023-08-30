# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.contacts.address_and_contact import load_address_and_contact
from frappe.contacts.address_and_contact import delete_contact_and_address
from frappe.model.document import Document

class Restaurant(Document):
	def validate(doc):
		if doc.jtt_id:
			jtt_doc = frappe.get_doc("JTT",doc.jtt_id)
			if doc.disable_jtt:
				if jtt_doc.disable == 0:
					jtt_doc.disable = 1
					jtt_doc.save()
			else:
				if jtt_doc.disable == 1:
					jtt_doc.disable = 0
					jtt_doc.save()
	def onload(self):
		"""Load address and contacts in `__onload`"""
		load_address_and_contact(self)
	def on_trash(self):
		delete_contact_and_address("Hotel Details", self.name)
