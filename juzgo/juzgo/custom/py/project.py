import frappe

@frappe.whitelist()
def get_project_abbr(project_name):
    m = project_name
    x = slice(3)
    return m[x].upper()