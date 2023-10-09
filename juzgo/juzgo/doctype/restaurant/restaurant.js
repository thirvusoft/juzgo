// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Restaurant', {
	open_url: function(frm){
        if(!frm.doc.pin_location){
            cur_frm.scroll_to_field('pin_location')
            frappe.throw('Enter Pin Location')
        }
        else{
        window.open(frm.doc.pin_location, '_blank')
        }
    },
    restaurant_name:function(frm){
        if (frm.doc.restaurant_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.restaurant_name,
                    "doctype": frm.doc.doctype,
                    "field": "restaurant_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "restaurant_name",
                            "description",
                            ('This Hotel Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/restaurant/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['restaurant_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "restaurant_name",
                "description",
                "");
        }
    },
    is_jtt: function(frm){
        if(frm.doc.is_jtt == 1){
            frappe.call({
                method: "juzgo.juzgo.doctype.hotel_details.hotel_details.jtt_creation",
                args: {
                    "name": frm.doc.name,
                    "doctype": frm.doc.doctype,
                    "user": frappe.session.user
                },
                callback: function (r) {
                    if(r.message){
                        frm.set_value("jtt_id",r.message)
                        frm.save()
                    }
                },
            })
        }
    },
    refresh: function(frm){
        frappe.dynamic_link = {doc: frm.doc, fieldname: 'name', doctype: 'Restaurant'}
        if (!frm.is_new()) {
			frappe.contacts.render_address_and_contact(frm);
		} else {
			frappe.contacts.clear_address_and_contact(frm);
		}
        frappe.call({
            method: "juzgo.juzgo.doctype.spots.spots.img_preview",
            args: {
                "table": frm.doc.image,
                "image":"image",
                "des":"description",
                "menu":"menu"
            },
            callback: function (r) {
               frm.set_df_property("img_preview","options",r.message)
            },
        })
        frappe.call({
            method: "juzgo.juzgo.doctype.spots.spots.img_preview",
            args: {
                "table": frm.doc.menu,
                "image":"image",
                "des":"description",
                "menu":"menu"
            },
            callback: function (r) {
               frm.set_df_property("menu_preview","options",r.message)
            },
        })

    },
});
// frappe.ui.form.on('Reference Table', {
// 	open_url: function(frm,cdt,cdn){
//         let row = locals[cdt][cdn]
//         if(!row.url){
//             frappe.throw('Enter URL in Row '+row.idx+' .')
//         }
//         else{
//         window.open(row.url, '_blank')
//         }
//     },
// })