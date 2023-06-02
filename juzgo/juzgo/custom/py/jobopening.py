import json
import frappe

@frappe.whitelist()
def get_staf_designation(staffing_plan=""):
    designation = []
    if staffing_plan:
        plan = frappe.get_doc("Staffing Plan", staffing_plan)
        for i in plan.get('staffing_details'):
            designation.append(i.designation)
        return designation
    else:
          return []

