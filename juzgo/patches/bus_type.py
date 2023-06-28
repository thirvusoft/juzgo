import frappe

def execute():
    bus_types = [
        "Sleeper", "Semi Sleeper", "Sitting", "Ac", "Non Ac", "Volvo only", "Volvo", "Scania", "Deluxe", "Economy bus"
    ]
    for bus_type in bus_types:
        if not frappe.db.exists("Bus Type", bus_type):
            doc = frappe.new_doc("Bus Type")
            doc.update({
                "bus_type": bus_type
            })
            doc.insert()
