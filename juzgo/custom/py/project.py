import frappe

def update_total(doc, event):
    total_sales_invoice = 0
    total_purchase_invoice = 0
    total_payment_pay = 0
    total_payment_receive = 0

    # Calculate total for custom_sales_invoice_table
    for row in doc.custom_sales_invocie_table:
        total_sales_invoice += float(row.grand_total)

    # Set the total value to the 'custom_sales_invoice_total_' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_sales_invoice_total_', total_sales_invoice)

    # Calculate total for custom_purchase_invoice_table
    for row in doc.custom_purchase_invocie_table:
        total_purchase_invoice += float(row.grand_total)

    # Set the total value to the 'custom_purchase_invoice_total' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_purchase_invoice_total', total_purchase_invoice)

    # Calculate total for custom_payment_pay_table
    for row in doc.custom_payment_pay_table:
        total_payment_pay += float(row.paid_amount)

    # Set the total value to the 'custom_payment_entry_pay_total_' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_payment_entry_pay_total', total_payment_pay)

    # Calculate total for custom_payment_receive_table
    for row in doc.custom_payment_receive_table:
        total_payment_receive += float(row.paid_amount)

    # Set the total value to the 'custom_payment_entry_receive_total_' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_payment_entry_receive_total', total_payment_receive)

    # Reload the document to reflect the changes
    doc.reload()


def update_net_total(doc, event):
    net_sales_invoice = 0
    net_purchase_invoice = 0
   

    # Calculate total for custom_sales_invoice_table
    for row in doc.custom_sales_invocie_table:
        net_sales_invoice += float(row.net_total)

    # Set the total value to the 'custom_sales_invoice_total_' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_sales_invoice_net_total', net_sales_invoice)

    # Calculate total for custom_purchase_invoice_table
    for row in doc.custom_purchase_invocie_table:
        net_purchase_invoice += float(row.net_total)

    # Set the total value to the 'custom_purchase_invoice_total' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_purchase_invoice_net_total', net_purchase_invoice)


    # Reload the document to reflect the changes
    doc.reload()


def update_tax_total(doc, event):
    tax_sales_invoice = 0
    tax_purchase_invoice = 0
   

    # Calculate total for custom_sales_invoice_table
    for row in doc.custom_sales_invocie_table:
        tax_sales_invoice += float(row.tax_and_charges)

    # Set the total value to the 'custom_sales_invoice_total_' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_sales_invoice_tax_and_charges_total', tax_sales_invoice)

    # Calculate total for custom_purchase_invoice_table
    for row in doc.custom_purchase_invocie_table:
        tax_purchase_invoice += float(row.tax_and_charges)

    # Set the total value to the 'custom_purchase_invoice_total' field in the Sales Invoice document
    frappe.db.set_value(doc.doctype, doc.name, 'custom_purchase_invoice_tax_and_charges_total', tax_purchase_invoice)


    # Reload the document to reflect the changes
    doc.reload()