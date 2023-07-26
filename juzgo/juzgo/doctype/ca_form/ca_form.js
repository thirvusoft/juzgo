// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('CA Form', {
	refresh: function(frm) {
		frm.set_query("suggested_spots", function () {
			var list = []
			frm.doc.interested_flavour.forEach(e => {
				list.push(e.flavour_type_name)
			});
			return {
				filters: {
					flavour_of_the_sopt : ['in',list],
				},
			};
		});
			frappe.call({
				method: "juzgo.juzgo.doctype.ca_form.ca_form.table_preview",
				callback: function (r) {
				   frm.set_df_property("passport_doc","options",r.message)
				},
			})
	},
});
