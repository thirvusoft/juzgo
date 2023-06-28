import frappe

def execute():
    quotas = [
        "Ladies Quota", "General Quota", "Tatkal Quota", "Senior citizen Quota"
    ]
    for quota in quotas:
        if not frappe.db.exists("Quota", quota):
            doc = frappe.new_doc("Quota")
            doc.update({
                "quota": quota
            })
            doc.insert()
