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
    update_value =[]
    if doc.branch:
        update_value.append("branch")
    if doc.project:
        update_value.append("project")
    if doc.cost_center:
        update_value.append("cost_center")
    if update_value:
        for i in doc.accounts:
            for update_field in update_value:
                i.update({update_field: doc.get(update_field)})