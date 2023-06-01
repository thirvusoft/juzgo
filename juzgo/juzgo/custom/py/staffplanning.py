import json
import frappe
from frappe.model.mapper import get_mapped_doc
from erpnext.stock.doctype.material_request.material_request import set_missing_values, update_item

@frappe.whitelist()
def make_job_opening(name,staffing_details):
    staffing_details = json.loads(staffing_details)
    c =1
    for i in staffing_details:
        if not frappe.db.exists("Job Opening",frappe.scrub(i.get('designation') or "").replace("_", "-")):
            c+=1
            document = frappe.new_doc("Job Opening")
            document.job_title =i.get('designation')
            document.designation =i.get('designation')
            document.staffing_plan =name
            document.save(ignore_permissions=True)
    return c
