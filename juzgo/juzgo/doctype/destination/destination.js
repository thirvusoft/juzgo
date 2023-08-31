// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Destination', {
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
                            ('This Hotel Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/destination/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['destination_name'] })
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
    spot:function(frm){
        window.open('/app/spots?is_jtt=1&destination='+frm.doc.name, '_blank')
    },
    hotel_details:function(frm){
        window.open('/app/hotel-details?is_jtt=1&destination='+frm.doc.name, '_blank')
    },
    restaurant:function(frm){
        window.open('/app/restaurant?is_jtt=1&destination='+frm.doc.name, '_blank')
    },
    refresh:function(frm){
        frappe.call({
            method: "juzgo.juzgo.doctype.destination.destination.connection",
            args: {
                "name": frm.doc.name,
            },
            callback: function (r) {
                console.log(r.message)
                if (r.message) {
                    frm.set_df_property("spot","label",r.message[0] > 0 ?`<span style="font-size: var(--text-xs);background-color: var(--gray-500);border-radius: var(--border-radius-sm);color: var(--gray-50);padding: 0 var(--padding-xs);margin-right: var(--margin-xs);">${r.message[0]}</span>`+" Spots":"Spots");
                    frm.set_df_property("hotel_details","label",r.message[1] > 0 ?`<span style="font-size: var(--text-xs);background-color: var(--gray-500);border-radius: var(--border-radius-sm);color: var(--gray-50);padding: 0 var(--padding-xs);margin-right: var(--margin-xs);">${r.message[1]}</span>`+" Hotel Details":"Hotel Details");
                    frm.set_df_property("restaurant","label",r.message[2] > 0 ?`<span style="font-size: var(--text-xs);background-color: var(--gray-500);border-radius: var(--border-radius-sm);color: var(--gray-50);padding: 0 var(--padding-xs);margin-right: var(--margin-xs);">${r.message[2]}</span>`+" Restaurant":"Restaurant");
                }
            },
        })
    }
    
});
