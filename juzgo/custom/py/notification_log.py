import frappe

def after_insert(doc,actions):
    frappe.publish_realtime("show_notification",{"doc":doc})