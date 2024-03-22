
import frappe

def make_entry(doc, method):
    project = frappe.get_doc("Project", doc.project)
    if project:
        project.append("custom_sales_invocie_table", {
            'sales_invoice': doc.name,
            'customer': doc.customer,
             "status" : doc.status,
            "posting_date": doc.posting_date,
            "net_total": doc.total,
            "tax_and_charges": doc.total_taxes_and_charges,
            "grand_total": doc.rounded_total
        })
        project.save()
        project.reload() 
    else:
        frappe.throw("Project not found or does not exist.") 


def delete_entry(doc, event):
    if doc.project:
        project = frappe.get_doc("Project", doc.project) 
        if project:
            try:
                for row in project.custom_sales_invocie_table:
                    if row.sales_invoice == doc.name:
                        project.custom_sales_invocie_table.remove(row)
                        break
                project.save()  # Save the changes
                project.reload()  # Reload the project document to reflect changes
            except Exception as e:
                frappe.log_error(f"Error deleting entry from custom table: {e}")
                frappe.msgprint("Error deleting entry from custom table. Please check the log for details.")
        else:
            frappe.msgprint("Project document not found.")
    else:
        frappe.msgprint("Project not linked to the document.")