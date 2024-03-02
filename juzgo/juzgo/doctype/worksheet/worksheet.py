# Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
import re

class Worksheet(Document):
    def validate(doc):
          cal_optional_tours(doc)

def cal_optional_tours(doc):

    doc.option_1_adult = doc.option_2_adult = doc.option_3_adult = doc.option_4_adult = doc.option_5_adult = doc.option_1_child = doc.option_2_child = doc.option_3_child = doc.option_4_child = doc.option_5_child = 0
    currency ={"INR":1}
    for i in doc.currency:
        currency[i.currency] = i.workout_based_on
    for i in doc.optional_tours:
        if i.option_1:
            doc.option_1_adult = doc.option_1_adult+ (i.adult * currency[i.currency])
            doc.option_1_child = doc.option_1_child+ (i.child * currency[i.currency])
        if i.option_2:
            doc.option_2_adult = doc.option_2_adult+ (i.adult * currency[i.currency])
            doc.option_2_child = doc.option_2_child+ (i.child * currency[i.currency])
        if i.option_3:
            doc.option_3_adult = doc.option_3_adult+ (i.adult * currency[i.currency])
            doc.option_3_child = doc.option_3_child+ (i.child * currency[i.currency])
        if i.option_4:
            doc.option_4_adult = doc.option_4_adult+ (i.adult * currency[i.currency])
            doc.option_4_child = doc.option_4_child+ (i.child * currency[i.currency])
        if i.option_5:
            doc.option_5_adult = doc.option_5_adult+ (i.adult * currency[i.currency])
            doc.option_5_child = doc.option_5_child+ (i.child * currency[i.currency])
    
    total_cost_price = 0
    for i in doc.complimentaries:
        total_cost_price += i.cost_price
    doc.total_cost_price = total_cost_price

    return doc
          
@frappe.whitelist()
def duplicate(option):
    old_option = frappe.get_doc("Worksheet Option",option)
    new_option = frappe.new_doc("Worksheet Option")
    new_option.worksheet = old_option.worksheet
    new_option.inclusions_worksheet = old_option.inclusions_worksheet
    new_option.cost_calculations = old_option.cost_calculations
    new_option.tour_manager_share = old_option.tour_manager_share
    new_option.total_in_inr = old_option.total_in_inr
    new_option.reduce_foc_cost_in_inr = old_option.reduce_foc_cost_in_inr
    new_option.final_total_amount = old_option.final_total_amount
    new_option.total_no_of_pax = old_option.total_no_of_pax
    new_option.amount_per_pax = old_option.amount_per_pax
    new_option.worksheet_name = increment_option_string(old_option.worksheet_name)
    new_option.save()
    return new_option    

def increment_option_string(input_str):
    def replace_numeric(match):
        return str(int(match.group()) + 1)

    result = re.sub(r'\b(\d+)\b', replace_numeric, input_str)
    
    return result