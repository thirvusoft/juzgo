# Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
import re
from juzgo.juzgo.doctype.worksheet_option.worksheet_option import final_calculate,_fetch_worksheet_details

class Worksheet(Document):
	def validate(doc):
		cal_optional_tours(doc)
		update_to_option(doc)

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
	option_1 = 0 
	option_2 = 0 
	option_3 = 0 
	option_4 = 0 
	option_5 = 0
	
	for i in doc.complimentaries:
		total_cost_price += i.cost_price
		if(i.option_1):
			option_1 += i.cost_price
		
		if(i.option_2):
			option_2 += i.cost_price
		
		if(i.option_3):
			option_3 += i.cost_price
		
		if(i.option_4):
			option_4 += i.cost_price
		
		if(i.option_5):
			option_5 += i.cost_price
		
	doc.total_cost_price = total_cost_price
	doc.complimentarie_option_1 = option_1
	doc.complimentarie_option_2 = option_2
	doc.complimentarie_option_3 = option_3
	doc.complimentarie_option_4 = option_4
	doc.complimentarie_option_5 = option_5
	

	return doc
		  
def update_to_option(doc):
	for i in doc.worksheet_options:
		wo=frappe.get_doc("Worksheet Option",i.options)
		final_calculate(wo)
		_fetch_worksheet_details(wo)
		wo.save()

@frappe.whitelist()
def duplicate(option):
	old_option = frappe.get_doc("Worksheet Option",option)
	new_option = frappe.new_doc("Worksheet Option")
	new_option.worksheet = old_option.worksheet
	# new_option.inclusions_worksheet = old_option.inclusions_worksheet
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

@frappe.whitelist()
def optional_tours(doc):
	doc=json.loads(doc)
	if doc.get('optional_tours'):
		option1=[]
		option2=[]
		option3=[]
		option4=[]
		option5=[]
		for opt in doc.get('optional_tours'):
			if opt.get('option_1'):
				option1.append(opt['optional_tours'])
			if opt.get('option_2'):
				option2.append(opt['optional_tours'])
			if opt.get('option_3'):
				option3.append(opt['optional_tours'])
			if opt.get('option_4'):
				option4.append(opt['optional_tours'])
			if opt.get('option_5'):
				option5.append(opt['optional_tours'])
		return option1, option2, option3, option4, option5

@frappe.whitelist()
def complementory(doc):
	doc=json.loads(doc)
	if doc.get('complimentaries'):
		opt_com1=[]
		opt_com2=[]
		opt_com3=[]
		opt_com4=[]
		opt_com5=[]
		for com in doc.get('complimentaries'):
			if com.get('option_1'):
				opt_com1.append(com['complimentaries'])
			if com.get('option_2'):
				opt_com2.append(com['complimentaries'])
			if com.get('option_3'):
				opt_com3.append(com['complimentaries'])
			if com.get('option_4'):
				opt_com4.append(com['complimentaries'])
			if com.get('option_5'):
				opt_com5.append(com['complimentaries'])
		return opt_com1, opt_com2, opt_com3, opt_com4, opt_com5

@frappe.whitelist()
def worksheet_inclusions(doc):
    doc = json.loads(doc)
    list =[]
    detail_list =[]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for work in worksheet.inclusions_worksheet:
                    if work.details not in detail_list:
                        detail_list.append(work.details)
                        list.append({work.details:[{"descriptions":work.descriptions,"option":worksheet.worksheet_name}]})
                    else:
                        for i in list:
                            for j in i:
                                if j == work.details:
                                    i[j].append({"descriptions":work.descriptions,"option":worksheet.worksheet_name})
        return list,detail_list

@frappe.whitelist()
def miscellenous_details(doc):
    doc = json.loads(doc)
    opt_mis = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for cost in worksheet.cost_calculations:
                    option_index = int(worksheet.worksheet_name[-1]) - 1
                    if cost.miscellaneous_in_inr:
                        opt_mis[option_index].append(f"{round(cost.miscellaneous_in_inr)}({cost.details})")

    return opt_mis[0], opt_mis[1], opt_mis[2], opt_mis[3], opt_mis[4]

@frappe.whitelist()
def worksheet_cost_calculations(doc):
    doc = json.loads(doc)
    list =[]
    detail_list =[]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for work in worksheet.cost_calculations:
                    if work.details not in detail_list:
                        detail_list.append(work.details)
                        list.append({work.details:[{"cost":round(work.sp_in_inr),"option":worksheet.worksheet_name}]})
                    else:
                        for i in list:
                            for j in i:
                                if j == work.details:
                                    i[j].append({"cost":round(work.sp_in_inr),"option":worksheet.worksheet_name})
        return list,detail_list				
@frappe.whitelist()
def adult_double(doc):
    doc = json.loads(doc)
    opt_alt_double = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for cost in worksheet.cost_calculations:
                    option_index = int(worksheet.worksheet_name[-1]) - 1
                    if cost.details == "Adult Double":
                        opt_alt_double[option_index].append(cost.sp_in_inr)

    return opt_alt_double[0], opt_alt_double[1], opt_alt_double[2], opt_alt_double[3], opt_alt_double[4]

@frappe.whitelist()
def adult_single(doc):
    doc = json.loads(doc)
    opt_alt_single = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for cost in worksheet.cost_calculations:
                    option_index = int(worksheet.worksheet_name[-1]) - 1
                    if cost.details == "Adult Single":
                        opt_alt_single[option_index].append(cost.sp_in_inr)

    return opt_alt_single[0], opt_alt_single[1], opt_alt_single[2], opt_alt_single[3], opt_alt_single[4]

@frappe.whitelist()
def adult_triple(doc):
    doc = json.loads(doc)
    opt_alt_triple = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for cost in worksheet.cost_calculations:
                    option_index = int(worksheet.worksheet_name[-1]) - 1
                    if cost.details == "Adult Triple":
                        opt_alt_triple[option_index].append(cost.sp_in_inr)

    return opt_alt_triple[0], opt_alt_triple[1], opt_alt_triple[2], opt_alt_triple[3], opt_alt_triple[4]

@frappe.whitelist()
def cnb(doc):
    doc = json.loads(doc)
    opt_cnb = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for cost in worksheet.cost_calculations:
                    option_index = int(worksheet.worksheet_name[-1]) - 1
                    if cost.details == "CNB":
                        opt_cnb[option_index].append(cost.sp_in_inr)

    return opt_cnb[0], opt_cnb[1], opt_cnb[2], opt_cnb[3], opt_cnb[4]

@frappe.whitelist()
def cwb(doc):
    doc = json.loads(doc)
    opt_cwb = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for acc in doc.get('worksheet_options'):
            if acc.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", acc['options'])
                for cost in worksheet.cost_calculations:
                    option_index = int(worksheet.worksheet_name[-1]) - 1
                    if cost.details == "CWB":
                        opt_cwb[option_index].append(cost.sp_in_inr)

    return opt_cwb[0], opt_cwb[1], opt_cwb[2], opt_cwb[3], opt_cwb[4]
	
@frappe.whitelist()
def option_link(doc):
    doc = json.loads(doc)
    name_opt = [[] for _ in range(5)]
    if doc.get('worksheet_options'):
        for opts in doc.get('worksheet_options'):
            if opts.get('options'):
                worksheet = frappe.get_doc("Worksheet Option", opts['options'])
                option_index = int(worksheet.worksheet_name[-1]) - 1
                name_opt[option_index].append(worksheet.name)
        return name_opt[0], name_opt[1], name_opt[2], name_opt[3], name_opt[4]

@frappe.whitelist()
def complimentaries_items():
    item_list=[]
    items=frappe.db.get_list("Item", filters={"disabled":0, "item_group":"Complimentaries"}, fields=["name", "item_name"])
    for item in items:
        if item.name:
            item_list.append(item.name)
    return item_list