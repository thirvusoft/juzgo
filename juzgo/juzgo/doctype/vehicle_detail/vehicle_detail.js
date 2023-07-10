// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Vehicle Detail', {
	vehicle_name:function(frm){
        if (frm.doc.vehicle_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.vehicle_name,
                    "doctype": frm.doc.doctype,
                    "field": "vehicle_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "vehicle_name",
                            "description",
                            ('This Hotel Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/vehicle-detail/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['vehicle_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "vehicle_name",
                "description",
                "");
        }
    },
});
