from frappe.model.naming import parse_naming_series, make_autoname
from frappe.model.naming import parse_naming_series
import frappe
def autoname(self,action):
    if self.branch == "Test":
        series = 'PI-TST-.YY.-'
        self.name = make_autoname(series, doc=self)
        self.naming_series = parse_naming_series(series, doc=self)
    else:
        series = 'PINV-.YY.-'
        self.name = make_autoname(series, doc=self)
        self.naming_series = parse_naming_series(series, doc=self)
        
def insert(self, action):
    if self.reference_name:
        doc = frappe.get_doc("Final Supplier Invoices in Project",self.reference_name)
        invoice_copy_file = frappe.get_doc({
            "doctype": "File",
            "file_name": f"{doc.supplier}-{self.project} Invoice Copy",
            "attached_to_doctype": "Purchase Invoice",  # Fix the typo in the field name
            "attached_to_name": self.name,
            "file_url": doc.invoice_copy
        }).insert()

        tt_agent_copy_file = frappe.get_doc({
            "doctype": "File",
            "file_name": f"{doc.tt_agent}-{self.project} TT Agent",
            "attached_to_doctype": "Purchase Invoice",  # Fix the typo in the field name
            "attached_to_name": self.name,
            "file_url": doc.tt_agent_copy
        }).insert()