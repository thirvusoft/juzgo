# Import frappe module
import frappe

# Define function to append Payment Receive record to Project
def make_entry(doc, method):
    if doc.doctype == "Payment Entry" and doc.payment_type == "Receive":
        project = frappe.get_doc("Project", doc.references[0].project)  # Assuming doc.project contains the Project ID
        project.append("custom_payment_receive_table", {
            'payment_entry': doc.name,
            'grand_total': doc.total_allocated_amount,
           
            "posting_date": doc.posting_date,
            "paid_amount": doc.paid_amount,  # Corrected typo here
            "mode_of_payment": doc.mode_of_payment
        })
        project.save()



    if doc.doctype == "Payment Entry" and doc.payment_type == "Pay":
        project = frappe.get_doc("Project", doc.references[0].project)  # Assuming doc.project contains the Project ID
        project.append("custom_payment_pay_table", {
            'payment_entry': doc.name,
            'grand_total': doc.total_allocated_amount,
            "status": "ok",
            "posting_date": doc.posting_date,
            "paid_amount": doc.paid_amount,  # Corrected typo here
            "mode_of_payment": doc.mode_of_payment
        })
        project.save()
