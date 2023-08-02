// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Missed Follow Up"] = {
	"filters": [
		{
			fieldname:'lead',
			label:'Lead',
			fieldtype:'Link',
			options:'Lead',
		},
		{
			fieldname:'next_followup_by',
			label:'Follow Up By',
			fieldtype:'Link',
			options:'User',
			default:frappe.session.user
		}
	]
};
