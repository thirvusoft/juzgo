import frappe

def get_context(context):
	print(context.web_form_fields)
	pass

@frappe.whitelist(allow_guest=True)
def get_designation():
	return frappe.get_all("Job Opening", {"status": "Open"}, ["name as label", "name as value"]) 