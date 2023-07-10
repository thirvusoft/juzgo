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
        frappe.call({
            method: "juzgo.juzgo.doctype.spots.spots.img_preview",
            args: {
                "table": frm.doc.image_table,
                "image":"image",
                "des":"image_name",
            },
            callback: function (r) {
               frm.set_df_property("img_preview","options",r.message)
            },
        })
	},
	open_website: function(frm){
        if(!frm.doc.website_link){
            cur_frm.scroll_to_field('website_link')
            frappe.throw('Enter WebSite Link')
        }
        else{
        window.open(frm.doc.website_link, '_blank')
        }
    },
	open_pin_location: function(frm){
        if(!frm.doc.pin_location){
            cur_frm.scroll_to_field('pin_location')
            frappe.throw('Enter Pin Location')
        }
        else{
        window.open(frm.doc.pin_location, '_blank')
        }
    },
    hotel_name:function(frm){
        if (frm.doc.hotel_name.length >= 3){
            frappe.call({
                method: "juzgo.juzgo.doctype.spots.spots.exist_list",
                args: {
                    "name": frm.doc.hotel_name,
                    "doctype": frm.doc.doctype,
                    "field": "hotel_name"
                },
                callback: function (r) {
                    if (r && r.message) {
                        frm.set_df_property(
                            "hotel_name",
                            "description",
                            ('This Hotel Name already exists: {0}', [r.message.map(function (d) {
                                return repl('<a href="/app/hotel-details/%(name)s">%(or_name)s</a>', { name: d['name'], or_name: d['hotel_name'] })
                            }).join(', ')]));
                    }
                },
            })
        } else {
            frm.set_df_property(
                "hotel_name",
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