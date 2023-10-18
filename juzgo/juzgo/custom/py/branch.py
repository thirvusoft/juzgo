import frappe
def validate(self,action):
    company_wise ={}
    throw_msg = ''
    for i in frappe.get_all("Company",pluck="name"):
        company_wise[i]=[]
    for i in self.naming_series:
        if i.naming_series_for not in company_wise[i.company]:
            company_wise[i.company].append(i.naming_series_for)
            if i.naming_series_for == "Sales Invoice":
                if len(i.naming_series) > 13 :
                    frappe.throw(f"#Row:{i.idx} is for Sales Invoice Naming Series. It's character count must be less then 14 then only GST Portal allow.")
        else:
            frappe.throw(f"#Row:{i.idx} is Duplicate.Remove this row.")
    for i in company_wise:
        set1 = set(["Sales Invoice","Purchase Invoice","Journal Entry","Payment Entry"])
        set2 = set(company_wise[i])
        missing_values = set1 - set2
        if missing_values:
            throw_msg = throw_msg + f"-> {i} company's Missing Naming Series:{str(missing_values)}<br>"
    
    if throw_msg != '':
        frappe.throw(throw_msg)