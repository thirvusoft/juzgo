from frappe.model.naming import parse_naming_series, make_autoname
from frappe.model.naming import parse_naming_series
import frappe
def autoname(self,action):
    if self.branch == "Test":
        series = 'TST-JV-.YYYY.-'
        self.name = make_autoname(series, doc=self)
        self.naming_series = parse_naming_series(series, doc=self)
    else:
        series = 'ACC-JV-.YYYY.-'
        self.name = make_autoname(series, doc=self)
        self.naming_series = parse_naming_series(series, doc=self)
def validate(doc,action):
    if doc.branch:
        for i in doc.accounts:
            i.branch = doc.branch