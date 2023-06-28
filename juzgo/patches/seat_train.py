import frappe

def execute():
    seats = [
        "Lower berth", "Upper berth", "Side Lower", "Side Upper", "Middle", "Any choice", "Window seat sitting"
    ]
    for seat in seats:
        if not frappe.db.exists("Seat Train", seat):
            doc = frappe.new_doc("Seat Train")
            doc.update({
                "seat": seat
            })
            doc.insert()
