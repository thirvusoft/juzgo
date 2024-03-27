// Copyright (c) 2024, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["TCS Payable Monthly"] = {
    "filters": [
        {
            "fieldname":"company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_default('company')
        },
        {
            "fieldname":"customer",
            "label": __("Customer"),
            "fieldtype": "Link",
            "options": "Customer",
          
        },
        {
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1,
            "width": "60px"
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1,
            "width": "60px"
        }
    ]
}
