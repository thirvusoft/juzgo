// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Followed Leads"] = {
	"filters": [
		{
			fieldname:'follow_date',
			label:'Follow Up Date',
			fieldtype:'Date',
			default:'Today'
		}
	]
};
