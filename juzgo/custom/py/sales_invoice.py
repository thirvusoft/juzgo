
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
    else:
        frappe.throw("Project not found or does not exist.") 