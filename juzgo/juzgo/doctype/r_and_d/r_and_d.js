// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('R and D', {
	destination_name:function(frm){
        if (frm.doc.destination_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.destination_name,
                    "doctype": frm.doc.doctype,
                    "field": "destination_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "destination_name",
                            "description",
                            ('This R and D Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/r-and-d/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['destination_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "destination_name",
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

