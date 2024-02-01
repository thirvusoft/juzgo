# Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	get_link_to_form
)

class DetailingPage(Document):
	def validate(self):
		self.fetch_customer()
	
	def fetch_customer(self):
		if self.project:
			customer_list = frappe.get_doc("Project",self.project)
			customer_list.multi_customer = []
			for i in customer_list.multi_customer:
				self.append("customer",dict(customer = i.customer))
		
