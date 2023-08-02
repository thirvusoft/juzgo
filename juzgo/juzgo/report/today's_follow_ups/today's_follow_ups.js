// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Today's Follow Ups"] = {
	"filters": [
		{
			fieldname:'follow_date',
			label:'Follow Up Date',
			fieldtype:'Date',
			default:'Today'
		}
	]
};
