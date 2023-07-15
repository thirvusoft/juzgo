import frappe

def after_insert(doc,actions):
    # if "Thirvu Admin" in frappe.get_roles:
    # user = frappe.session.user
    # if not frappe.db.get_value('User', user, 'notify'):
    #     return
    frappe.publish_realtime("show_notification",{"doc":doc})