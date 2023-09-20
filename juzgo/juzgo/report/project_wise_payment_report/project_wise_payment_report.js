// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project-Wise Payment Report"] = {
	"filters": [
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
			"reqd": 1
		},
		{
			"fieldname":"project",
			"label": __("Project"),
			"fieldtype": "Link",
			"options": "Project",
		},
		{
			"fieldname":"party_type",
			"label": __("Party Type"),
			"fieldtype": "Autocomplete",
			options: ["Supplier","Customer"],
			on_change: function() {
				frappe.query_report.set_filter_value('party', "");
			}
		},
		{
			"fieldname":"party",
			"label": __("Party"),
			"fieldtype": "MultiSelectList",
			get_data: function(txt) {
				if (!frappe.query_report.filters) return;

				let party_type = frappe.query_report.get_filter_value('party_type');
				if (!party_type) return;

				return frappe.db.get_link_options(party_type, txt);
			},
			on_change: function() {
				var party_type = frappe.query_report.get_filter_value('party_type');
				var parties = frappe.query_report.get_filter_value('party');

				if(!party_type || parties.length === 0 || parties.length > 1) {
					frappe.query_report.set_filter_value('party_name', "");
					return;
				} else {
					var party = parties[0];
					var fieldname = erpnext.utils.get_party_name(party_type) || "name";
					frappe.db.get_value(party_type, party, fieldname, function(value) {
						frappe.query_report.set_filter_value('party_name', value[fieldname]);
					});
				}
			}
		},
		{
			"fieldname":"party_name",
			"label": __("Party Name"),
			"fieldtype": "Data",
			"hidden": 1
		},
		
		{
			"fieldname":"purchase_invoice",
			"label": __("Purchase Invoice"),
			"fieldtype": "Check",
			"default":1,
		},
		{
			"fieldname":"sales_invoice",
			"label": __("Sales Invoice"),
			"fieldtype": "Check",
			"default":1,
		},
		{
			"fieldname":"sales_payment_entry",
			"label": __("Sales Payment Entry"),
			"fieldtype": "Check",
			"default":1,
		},
		{
			"fieldname":"purchase_payment_entry",
			"label": __("Purchase Payment Entry"),
			"fieldtype": "Check",
			"default":1,
		},
		{
			"fieldname":"delivery_note",
			"label": __("Delivery Note"),
			"fieldtype": "Check",
			"default":1,
		},
	]
}
