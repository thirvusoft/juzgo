// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bus', {
	refresh: function(frm) {
		frappe.call({
            method: "juzgo.juzgo.doctype.spots.spots.img_preview",
            args: {
                "table": frm.doc.bus_images,
                "image":"image",
                "des":"description",
            },
            callback: function (r) {
               frm.set_df_property("img_preview","options",r.message)
            },
        })
	}
});
