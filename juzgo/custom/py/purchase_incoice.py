
import frappe

def make_entry(doc, method):
    project = frappe.get_doc("Project", doc.project)
    if project:
        project.append("custom_purchase_invocie_table", {
            'purchase_invoice': doc.name,
            "status" : doc.status,
            'supplier': doc.supplier,
            "posting_date": doc.posting_date,
            "net_total": doc.total,
            "tax_and_charges": doc.total_taxes_and_charges,
            "grand_total": doc.rounded_total
        })
        project.save()
    else:
        frappe.throw("Project not found or does not exist.")  # Handle case when project is None


import frappe

def delete_entry(doc, event):
    if doc.project:
        project = frappe.get_doc("Project", doc.project) 
        if project:
            try:
                for row in project.custom_purchase_invocie_table:
                    if row.purchase_invoice == doc.name:
                        project.custom_purchase_invocie_table.remove(row)
                        break
                project.save()  # Save the changes
                project.reload()  # Reload the project document to reflect changes
                frappe.msgprint("Entry removed from custom table in Project document.")
            except Exception as e:
                frappe.log_error(f"Error deleting entry from custom table: {e}")
                frappe.msgprint("Error deleting entry from custom table. Please check the log for details.")
        else:
            frappe.msgprint("Project document not found.")
    else:
        frappe.msgprint("Project not linked to the document.")

