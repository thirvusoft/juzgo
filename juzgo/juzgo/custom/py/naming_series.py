from frappe.model.naming import parse_naming_series, make_autoname
import frappe
def autoname(self,action):
    if self.branch and self.company:
        branch = frappe.get_doc("Branch",self.branch)
        if branch.set_default_naming_series == 0:
            for i in branch.naming_series:
                if self.company == i.company and self.doctype == i.naming_series_for:
                    series = i.naming_series
                    self.name = make_autoname(series, doc=self)
                    self.naming_series = series
