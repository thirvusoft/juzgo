# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document

class CheckList(Document):
	def autoname(self):
		check_list_for = "CUS" if self.check_list_for == "Customer" else self.destination_name
		gender = "M" if self.gender=="Male" else "F" if self.gender=="Female" else "B"
		self.name = check_list_for + "-" + gender + "-" + str(self.age_limit_from) + "-" + str(self.age_limit_to)
