# Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_link_to_form
class CheckList(Document):
	def autoname(self):
		destination = ''
		for i in self.destination_name:
			destination += frappe.get_value('Destination',i.destination,"destination_abbr") or i.destination
			destination += "-"
		check_list_for = "CUS-" if self.check_list_for == "Customer" else "PP-" if self.check_list_for == "Passport" else "Visa-"+destination if self.check_list_for == "Visa" else destination
		gender = "M" if self.gender=="Male" else "F" if self.gender=="Female" else "B"
		self.name = check_list_for + gender + "-" + str(self.age_limit_from) + "-" + str(self.age_limit_to)
	def validate(self):
		validate_if_new(self)

def validate_if_new(self):
	if self.age_limit_from > self.age_limit_to:
		frappe.throw("Kindly Check Age Limit from is Greater then Age Limit To.")
	all_doc = frappe.get_all("Check List",filters={"disable":0,"name":['not in',self.name]})
	for i in all_doc:
		doc = frappe.get_doc("Check List",i.name)
		if doc.check_list_for == "Customer" and self.check_list_for == "Customer":
			validate_overlap(doc,self)
		if doc.check_list_for == "Passport" and self.check_list_for == "Passport":
			validate_overlap(doc,self)
		if (doc.check_list_for == "Destination" and self.check_list_for == "Destination") or (doc.check_list_for == "Visa" and self.check_list_for == "Visa"):
			# Multi select of Destination
			for i in doc.destination_name:
				for j in self.destination_name:
					if i.destination == j.destination:
						validate_overlap(doc,self)
			# Single select of Destination
			# if doc.destination_name == self.destination_name:
			# 	validate_overlap(doc,self)
			

def validate_overlap(doc,self):
	if doc.gender == self.gender or "Both" == self.gender or "Both" == doc.gender:
		if (
			((self.age_limit_from >= doc.age_limit_from) and (self.age_limit_from <= doc.age_limit_to))
			or ((self.age_limit_to >= doc.age_limit_from) and (self.age_limit_to <= doc.age_limit_to))
			or ((self.age_limit_from <= doc.age_limit_from) and (self.age_limit_to >= doc.age_limit_to))
		):
			frappe.throw("Age Is Overlap Kindly Check with "+get_link_to_form('Check List',doc.name))
