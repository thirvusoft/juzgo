# Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
import json
from frappe.model.document import Document

class WorksheetOption(Document):
	def validate(doc):
		final_calculate(doc)
		_fetch_worksheet_details(doc)

def final_calculate(doc):
	total_price = 0
	for i in doc.tour_manager_share:
		total_price += i.amount_in_inr or 0

	doc.total_in_inr = total_price
	doc.final_total_amount =((doc.total_in_inr or 0) - (doc.reduce_foc_cost_in_inr or 0))
	doc.amount_per_pax = ((doc.final_total_amount or 0) / (doc.total_no_of_pax or 1))

@frappe.whitelist()
def fetch_default_value(doc):
	doc = json.loads(doc)
	cost_calculations = frappe.get_all("Cost Calculations Category",filters={"default":1},pluck="name")
	tour_manager_share_item = frappe.get_all("Tour Manager Share Item",filters={"default":1},pluck="name")					
	currency ={}
	ws = frappe.get_doc("Worksheet",doc.get("worksheet"))
	for i in ws.currency:
		currency[i.currency] = i.workout_based_on
	return cost_calculations, tour_manager_share_item, inclusions_worksheet(doc), currency

def inclusions_worksheet(doc):
	dp = frappe.get_doc("Detailing Page",doc.get("detailing_page"))
	inclusions_worksheet = []
	descriptions = ""
	s_no = 0
	for i in dp.hotels:
		if i.options == doc.get("worksheet_name") and  i.hotel_name:
			s_no += 1
			descriptions += str(s_no)+". "+i.hotel_name
			if i.room_category:
				descriptions += f"({i.room_category})"

			if i.meal_preference:
				descriptions += f"and Meal Plan is {i.meal_preference}"

			if i.no_of_nights or i.no_of_days:
				descriptions += f"for {i.no_of_nights} Nights {i.no_of_days} days.\n"
	inclusions_worksheet.append({"details":"Accommodation Details","descriptions":descriptions})

	descriptions = ""
	s_no = 0
	for i in dp.spots:
		if i.options == doc.get("worksheet_name") and  i.spots:
			s_no += 1
			descriptions += str(s_no)+". "+i.spots
			if i.transfer_type:
				descriptions += f"on {i.transfer_type}.\n"
	inclusions_worksheet.append({"details":"Sightseeing Details","descriptions":descriptions})

	descriptions = ""
	s_no = 0
	for i in dp.vehicle:
		if i.options == doc.get("worksheet_name") and  i.vehicle:
			s_no += 1
			descriptions += str(s_no)+". "+i.vehicle
			if i.transfer_type:
				descriptions += f"on {i.transfer_type}.\n"
	inclusions_worksheet.append({"details":"Vehicle Details","descriptions":descriptions})

	descriptions = ""
	s_no = 0
	for i in dp.others:
		if i.others:
			s_no += 1
			descriptions += str(s_no)+". "+i.others+".\n"
		
	inclusions_worksheet.append({"details":"Others Details","descriptions":descriptions})

	# descriptions = ""
	# s_no = 0
	# for i in dp.optional_costs:
	# 	if i.spots:
	# 		s_no += 1
	# 		descriptions += str(s_no)+". "+i.spots+".\n"
	# 		if i.transfer_type:
	# 			descriptions += f"on {i.transfer_type}.\n"
	# inclusions_worksheet.append({"details":"Optional costs","descriptions":descriptions})						
					

	return inclusions_worksheet

@frappe.whitelist()
def fetch_worksheet_details(doc):
	doc = json.loads(doc)
	ws= frappe.get_doc("Worksheet",doc.get("worksheet"))
	for i in doc.get('cost_calculations'):
		age_type = frappe.get_value("Cost Calculations Category",i.get("details"),"age_category")
		i["optional_tours_in_inr"] = (ws.get(doc.get("worksheet_name").lower().replace(" ", "_")+"_"+age_type.lower()))/(frappe.get_value("Cost Calculations Category",i.get("details"),"share") or 1)
		i["complimentaries_in_inr"] = ws.get("complimentarie_"+doc.get("worksheet_name").lower().replace(" ", "_"))
	return doc.get('cost_calculations')

def _fetch_worksheet_details(doc):
	ws= frappe.get_doc("Worksheet",doc.get("worksheet"))
	currency ={}
	for i in ws.currency:
		currency[i.currency] = i.workout_based_on
	for i in doc.get('cost_calculations'):
		age_type = frappe.get_value("Cost Calculations Category",i.get("details"),"age_category")
		i.optional_tours_in_inr = (ws.get(doc.get("worksheet_name").lower().replace(" ", "_")+"_"+age_type.lower()))/(frappe.get_value("Cost Calculations Category",i.get("details"),"share") or 1)
		i.complimentaries_in_inr = ws.get("complimentarie_"+doc.get("worksheet_name").lower().replace(" ", "_"))
		i.cp_in_inr = (i.total_in_inr or 0)+(i.optional_tours_in_inr or 0)+(i.complimentaries_in_inr or 0)+(i.miscellaneous_in_inr or 0)
		i.sp_in_inr  = (i.cp_in_inr or 0)+(i.margins or 0)
	
	return doc.get('cost_calculations')
