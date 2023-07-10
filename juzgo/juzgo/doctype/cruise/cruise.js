// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Cruise', {
	cruise_name:function(frm){
        if (frm.doc.cruise_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.cruise_name,
                    "doctype": frm.doc.doctype,
                    "field": "cruise_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "cruise_name",
                            "description",
                            ('This Hotel Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/cruise/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['cruise_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "cruise_name",
                "description",
                "");
        }
    },
});

frappe.ui.form.on('Reference Table', {
	open_url: function(frm,cdt,cdn){
        let row = locals[cdt][cdn]
        if(!row.url){
            frappe.throw('Enter URL in Row '+row.idx+' .')
        }
        else{
        window.open(row.url, '_blank')
        }
    },
})