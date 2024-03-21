
import frappe

def make_entry(doc, method):
    project = frappe.get_doc("Project", doc.project)
    if project:
        project.append("custom_purchase_invocie_table", {
            'payment_invoice': doc.name,
            'supplier': doc.supplier,
            "posting_date": doc.posting_date,
            "net_total": doc.total,
            "tax_and_charges": doc.total_taxes_and_charges,
            "grand_total": doc.rounded_total
        })
        project.save()
    else:
        frappe.throw("Project not found or does not exist.")  # Handle case when project is None
