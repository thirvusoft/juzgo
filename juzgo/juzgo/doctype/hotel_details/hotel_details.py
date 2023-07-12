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