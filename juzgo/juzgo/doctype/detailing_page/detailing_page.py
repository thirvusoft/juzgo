# Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import (
	get_link_to_form
)
import random

class DetailingPage(Document):
	def validate(self):
		self.fetch_customer()
		self.fetch_destination()
		self.spots_adding()
		if self.project:
			caform=frappe.db.get_value("Project", self.project, "ca_form")
			if caform:
				self.ca_form=caform

		

	def fetch_customer(self):
		if self.project:
			customer_list = frappe.get_doc("Project",self.project)
			multi_customer = []
			for i in customer_list.multi_customer:
				multi_customer.append({"customer":i.customer})
			self.update({"customer": multi_customer})

	def fetch_destination(self):
		destination_l = []
		destination = []
		if self.project:
			project_name = frappe.get_doc("Project",self.project)
			for i in project_name.destination:
				destination_l.append({'destination_name': i.destination_name})
				destination.append(i.destination_name)
		if self.ca_form:
			ca_dest=frappe.db.get_value("CA Form", self.ca_form, "freezed_destination")
			if ca_dest not in destination:
				destination_l.append({'destination_name': ca_dest})
		self.update({"destination": destination_l})
		
	def spots_adding(self):
		if self.destination and len(self.spots) == 0:
			detail_spot=[]
			for dest in self.destination:
				spot_list=frappe.get_doc("Destination", dest.destination_name)
				if spot_list:
					for spot in spot_list.default_spots:
						det_id = random.randint(0,9)
						detail_spot.append({'options': "Option 1", 'spots':spot.spots_name, 'det_id':det_id})
						detail_spot.append({'options': "Option 2", 'det_id':det_id})
						detail_spot.append({'options': "Option 3", 'det_id':det_id})
						detail_spot.append({'options': "Option 4", 'det_id':det_id})
						detail_spot.append({'options': "Option 5", 'det_id':det_id})
					self.update({"spots": detail_spot})
     
@frappe.whitelist()
def ca_form_details(ca_form):
    ca_forms=frappe.db.get_list("CA Form", filters={"name":ca_form}, fields=["travel_start_date", "travel_end_date", "no_of_adult", "no_of_childrens", "child_without_bed"])
    return ca_forms
