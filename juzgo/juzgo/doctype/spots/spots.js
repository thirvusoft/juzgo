// Copyright (c) 2023, Thirvusoft Pvt Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on('Spots', {
    // validate: function(frm){
    //     if((frm.doc.opening_time.split(':')[0] == frm.doc.closing_time.split(':')[0])&&(frm.doc.opening_time.split(':')[1] == frm.doc.closing_time.split(':')[1])){
    //         frappe.throw("Kindly Check Opening Time and Closing Time. Both Time cannot be same.")
    //     }
    // },
	open_url: function(frm){
        if(!frm.doc.pin_location){
            cur_frm.scroll_to_field('pin_location')
            frappe.throw('Enter Pin Location')
        }
        else{
        window.open(frm.doc.pin_location, '_blank')
        }
    },
    open_website: function(frm){
        if(!frm.doc.website_url){
            cur_frm.scroll_to_field('website_url')
            frappe.throw('Enter Website')
        }
        else{
        window.open(frm.doc.website_url, '_blank')
        }
    },
    refresh: function(frm){
        frappe.call({
            method: "juzgo.juzgo.doctype.spots.spots.img_preview",
            args: {
                "table": frm.doc.image_details,
                "image":"image",
                "des":"description",
            },
            callback: function (r) {
               frm.set_df_property("img_preview","options",r.message)
            },
        })
        if(frm.is_new()){
            frm.set_value("working_days",[{"days":"Monday"},{"days":"Thursday"},{"days":"Wednesday"},{"days":"Thursday"},{"days":"Friday"},{"days":"Saturday"},{"days":"Sunday"}])
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
    spot_name:function(frm){
        if (frm.doc.spot_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.spot_name,
                    "doctype": frm.doc.doctype,
                    "field": "spot_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "spot_name",
                            "description",
                            ('This Spots Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/spots/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['spot_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "spot_name",
                "description",
                "");
        }
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