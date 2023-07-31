import frappe

def execute():
    auto_repeats = frappe.get_all("Auto Repeat")
    for ar in auto_repeats:
        doc = frappe.get_doc("Auto Repeat", ar.name)
        doc.set_dates()
        doc.db_update()
