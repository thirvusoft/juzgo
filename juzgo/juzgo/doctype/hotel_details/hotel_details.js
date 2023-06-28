// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hotel Details', {
	refresh: function(frm) {
		frm.set_query("nearby_places_table", function () {
			return { filters:{destination: frm.doc.destination }};
		});
		frm.set_query("nearby_indian_restaurants", function () {
			return { filters:{type: "India" }};
		});
	}
});
