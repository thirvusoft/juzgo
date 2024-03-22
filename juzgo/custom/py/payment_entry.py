# Import frappe module
import frappe

# Define function to append Payment Receive record to Project
def make_entry(doc, method):
    if doc.doctype == "Payment Entry" and doc.payment_type == "Receive":
        project_name = ""
        if doc.references and doc.references[0].project:
            project_name = doc.references[0].project
        elif doc.project:
            project_name = doc.project
        project = frappe.get_doc("Project", project_name)  # Assuming doc.project contains the Project ID
        project.append("custom_payment_receive_table", {
            'payment_entry': doc.name,
            'grand_total': doc.total_allocated_amount,
             "status" : doc.status,
            "posting_date": doc.posting_date,
            "paid_amount": doc.paid_amount,  # Corrected typo here
            "mode_of_payment": doc.mode_of_payment
        })
        project.save()



    if doc.doctype == "Payment Entry" and doc.payment_type == "Pay":
        project_name = ""
        if doc.references and doc.references[0].project:
            project_name = doc.references[0].project
        elif doc.project:
            project_name = doc.project
        project = frappe.get_doc("Project", project_name)  # Assuming doc.project contains the Project ID
        project.append("custom_payment_pay_table", {
            'payment_entry': doc.name,
            'grand_total': doc.total_allocated_amount,
            "status" : doc.status,
            "posting_date": doc.posting_date,
            "paid_amount": doc.paid_amount,  # Corrected typo here
            "mode_of_payment": doc.mode_of_payment
        })
        project.save()

def remove_entry(doc, event):
    project_name = ""
    if doc.references and doc.references[0].project:
        project_name = doc.references[0].project
    elif doc.project:
        project_name = doc.project

    if project_name:
        project = frappe.get_doc("Project", project_name) 
        if project:
            if doc.payment_type == "Pay":
                for row in project.custom_payment_pay_table:
                    if row.payment_entry == doc.name:
                        project.custom_payment_pay_table.remove(row)
                        break  
            elif doc.payment_type == "Receive":
                for row in project.custom_payment_receive_table:
                    if row.payment_entry == doc.name:
                        project.custom_payment_receive_table.remove(row)
                        break  
            else:
                frappe.msgprint("Invalid payment type: {}".format(doc.payment_type))
                
            project.save() 
            project.reload()
          

    


