import frappe

def after_insert(doc,actions):
    # if "Thirvu Admin" in frappe.get_roles:
    frappe.publish_realtime("show_notification",{"doc":doc})