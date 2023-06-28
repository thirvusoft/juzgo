import frappe

def execute():
    coaches = [
        "2nd Sleeper", "2nd Sitting", "2 Tier AC", "3 Tier AC", "Chair car", "1 Tier AC"
    ]
    for coach in coaches:
        if not frappe.db.exists("Coach", coach):
            doc = frappe.new_doc("Coach")
            doc.update({
                "coach": coach
            })
            doc.insert()
