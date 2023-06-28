import frappe

def execute():
    mode_of_transports = [
        "Flight", "Train", "Bus", "Land Transport", "Cruise"
    ]
    for mot in mode_of_transports:
        if not frappe.db.exists("Mode Of Transport", mot):
            doc = frappe.new_doc("Mode of Transport")
            doc.update({
                "mode_of_transport": mot
            })
            doc.insert()
